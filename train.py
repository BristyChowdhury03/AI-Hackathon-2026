import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error


def find_dataset() -> Path:
    candidates = [
        Path("hackathon_preli_dataset - bangladesh_dengue_large_dataset.csv"),
        Path("dataset/hackathon_preli_dataset - bangladesh_dengue_large_dataset.csv"),
        Path("hackathon_preli_dataset - bangl.xlsx"),
        Path("dataset/hackathon_preli_dataset - bangl.xlsx"),
    ]
    for p in candidates:
        if p.exists():
            return p
    for folder in [Path("."), Path("dataset")]:
        if folder.exists():
            for ext in ("*.csv", "*.xlsx", "*.xls"):
                files = list(folder.glob(ext))
                if files:
                    return files[0]
    raise FileNotFoundError("Dataset file not found in root or dataset/ folder.")


def ensure_col(df: pd.DataFrame, col: str, default_val: float) -> pd.Series:
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    return pd.Series(default_val, index=df.index, dtype="float64")


def parse_dates_safely(series: pd.Series) -> pd.Series:
    parsed = pd.to_datetime(series, errors="coerce")
    if parsed.notna().sum() == 0:
        parsed = pd.to_datetime(series, errors="coerce", dayfirst=True)
    if parsed.notna().sum() == 0:
        return pd.Series(
            pd.date_range("2023-01-01", periods=len(series), freq="D"),
            index=series.index,
        )
    fallback_dates = pd.Series(
        pd.date_range("2023-01-01", periods=len(series), freq="D"),
        index=series.index,
    )
    return parsed.fillna(fallback_dates)


def load_raw_data(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)

    df.columns = [str(c).strip().lower() for c in df.columns]
    if df.empty:
        raise ValueError(f"Dataset '{path.name}' is empty.")

    date_col = next(
        (c for c in ["date", "week_start", "report_date", "timestamp", "month", "year"] if c in df.columns),
        None,
    )
    if date_col:
        df["date"] = parse_dates_safely(df[date_col])
    else:
        df["date"] = pd.date_range("2023-01-01", periods=len(df), freq="D")

    ward_col = next((c for c in ["ward_id", "ward", "ward_no", "zone_id", "district"] if c in df.columns), None)
    if ward_col:
        numeric_ward = pd.to_numeric(df[ward_col], errors="coerce")
        if numeric_ward.notna().any():
            df["ward_id"] = numeric_ward.fillna(0).astype(int)
        else:
            df["ward_id"] = pd.factorize(df[ward_col].astype(str))[0] + 1
    else:
        df["ward_id"] = 1

    max_t = ensure_col(df, "max_temp", 32.0)
    min_t = ensure_col(df, "min_temp", 25.0)
    avg_t = ensure_col(df, "avg_temp", np.nan)
    df["avg_temp"] = avg_t.fillna((max_t + min_t) / 2.0).ffill().bfill().fillna(28.0)

    df["rainfall_mr"] = ensure_col(df, "rainfall_mr", 0.0)
    rain_alt = ensure_col(df, "rainfall", np.nan)
    df["rainfall_mr"] = df["rainfall_mr"].where(df["rainfall_mr"].notna(), rain_alt).fillna(0.0)

    df["relative_hu"] = ensure_col(df, "relative_hu", np.nan)
    hum_alt = ensure_col(df, "humidity", np.nan)
    df["relative_hu"] = (
        df["relative_hu"]
        .where(df["relative_hu"].notna(), hum_alt)
        .ffill()
        .bfill()
        .fillna(75.0)
    )

    cases_col = next((c for c in ["dengue_cases", "cases", "dengue_case"] if c in df.columns), None)
    df["dengue_cases"] = (
        pd.to_numeric(df[cases_col], errors="coerce").fillna(0.0) if cases_col else 0.0
    )

    df["population"] = ensure_col(df, "population", 50000.0)
    df["water_logg"] = ensure_col(df, "water_logg", 0.4)
    df["sanitation"] = ensure_col(df, "sanitation", 0.6)

    for vuln_col in ["population", "water_logg", "sanitation"]:
        med = df[vuln_col].median()
        fallback = 0.5 if pd.isna(med) else float(med)
        df[vuln_col] = (
            df.groupby("ward_id")[vuln_col]
            .transform(lambda s: s.ffill().bfill())
            .fillna(fallback)
        )

    return df.sort_values(["ward_id", "date"]).reset_index(drop=True)


def build_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    g = out.groupby("ward_id", group_keys=False)

    for days in (7, 14, 21, 28):
        out[f"rain_sum_{days}d"] = g["rainfall_mr"].transform(
            lambda s: s.shift(1).rolling(days, min_periods=1).sum()
        )
        out[f"rain_mean_{days}d"] = g["rainfall_mr"].transform(
            lambda s: s.shift(1).rolling(days, min_periods=1).mean()
        )
        out[f"temp_mean_{days}d"] = g["avg_temp"].transform(
            lambda s: s.shift(1).rolling(days, min_periods=1).mean()
        )
        out[f"humidity_mean_{days}d"] = g["relative_hu"].transform(
            lambda s: s.shift(1).rolling(days, min_periods=1).mean()
        )

    out["target_cases_14d"] = g["dengue_cases"].transform(
        lambda s: s.shift(-1).rolling(14, min_periods=1).sum()
    )

    feature_cols = [
        "population",
        "water_logg",
        "sanitation",
        "avg_temp",
        "rainfall_mr",
        "relative_hu",
        "rain_sum_7d",
        "rain_sum_14d",
        "rain_sum_21d",
        "rain_sum_28d",
        "rain_mean_7d",
        "rain_mean_14d",
        "rain_mean_21d",
        "rain_mean_28d",
        "temp_mean_7d",
        "temp_mean_14d",
        "temp_mean_21d",
        "temp_mean_28d",
        "humidity_mean_7d",
        "humidity_mean_14d",
        "humidity_mean_21d",
        "humidity_mean_28d",
    ]
    out[feature_cols] = out[feature_cols].fillna(0.0)
    return out


def main() -> None:
    dataset_path = find_dataset()
    raw_df = load_raw_data(dataset_path)
    feat_df = build_lag_features(raw_df)

    feature_cols = [
        "population",
        "water_logg",
        "sanitation",
        "avg_temp",
        "rainfall_mr",
        "relative_hu",
        "rain_sum_7d",
        "rain_sum_14d",
        "rain_sum_21d",
        "rain_sum_28d",
        "rain_mean_7d",
        "rain_mean_14d",
        "rain_mean_21d",
        "rain_mean_28d",
        "temp_mean_7d",
        "temp_mean_14d",
        "temp_mean_21d",
        "temp_mean_28d",
        "humidity_mean_7d",
        "humidity_mean_14d",
        "humidity_mean_21d",
        "humidity_mean_28d",
    ]

    unique_dates = sorted(feat_df["date"].dropna().unique())
    if len(unique_dates) >= 2:
        split_idx = max(1, min(len(unique_dates) - 1, int(len(unique_dates) * 0.8)))
        cutoff_date = unique_dates[split_idx - 1]
        train_df = feat_df[feat_df["date"] <= cutoff_date]
        test_df = feat_df[feat_df["date"] > cutoff_date]
        if test_df.empty:
            test_df = train_df.tail(max(1, len(train_df) // 5))
    else:
        cutoff_date = unique_dates[0] if unique_dates else pd.Timestamp("2023-01-01")
        train_df = feat_df
        test_df = feat_df.tail(max(1, len(feat_df) // 5))

    X_train, y_train = train_df[feature_cols], train_df["target_cases_14d"]
    X_test, y_test = test_df[feature_cols], test_df["target_cases_14d"]

    model = HistGradientBoostingRegressor(
        max_iter=200,
        learning_rate=0.05,
        max_depth=6,
        random_state=42,
    )
    model.fit(X_train, y_train)

    preds_test = np.clip(model.predict(X_test), 0, None)
    mae = float(mean_absolute_error(y_test, preds_test))
    rmse = float(root_mean_squared_error(y_test, preds_test))

    p95_val = float(np.percentile(feat_df["target_cases_14d"], 95))
    risk_scale_cap = max(p95_val, 1.0)

    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    joblib.dump(model, models_dir / "dengue_model.pkl")

    ward_profiles = {}
    for wid, wdf in feat_df.groupby("ward_id"):
        latest = wdf.iloc[-1]
        city_val = (
            str(latest["city"])
            if "city" in wdf.columns and pd.notna(latest["city"])
            else "Ward"
        )
        ward_profiles[str(int(wid))] = {
            "ward_id": int(wid),
            "city": city_val,
            "population": float(latest["population"]),
            "water_logg": float(latest["water_logg"]),
            "sanitation": float(latest["sanitation"]),
            "avg_temp": float(latest["avg_temp"]),
            "rainfall_mr": float(latest["rainfall_mr"]),
            "relative_hu": float(latest["relative_hu"]),
            "rain_sum_7d": float(latest["rain_sum_7d"]),
            "rain_sum_14d": float(latest["rain_sum_14d"]),
            "rain_sum_21d": float(latest["rain_sum_21d"]),
            "rain_sum_28d": float(latest["rain_sum_28d"]),
            "temp_mean_14d": float(latest["temp_mean_14d"]),
            "humidity_mean_14d": float(latest["humidity_mean_14d"]),
        }

    meta = {
        "dataset_file": dataset_path.name,
        "feature_cols": feature_cols,
        "cutoff_date": str(pd.Timestamp(cutoff_date).date()),
        "train_rows": int(len(train_df)),
        "test_rows": int(len(test_df)),
        "mae_14d": round(mae, 3),
        "rmse_14d": round(rmse, 3),
        "risk_scale_cap": risk_scale_cap,
        "ward_profiles": ward_profiles,
    }
    (models_dir / "model_meta.json").write_text(json.dumps(meta, indent=2))
    print(f"Trained on {dataset_path.name} | MAE={mae:.3f}, RMSE={rmse:.3f}")


if __name__ == "__main__":
    main()