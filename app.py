import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="DengueGuard AI",
    page_icon="🦟",
    layout="wide",
)


@st.cache_resource
def load_artifacts():
    model_path = Path("models/dengue_model.pkl")
    meta_path = Path("models/model_meta.json")
    if not model_path.exists() or not meta_path.exists():
        return None, None
    return joblib.load(model_path), json.loads(meta_path.read_text())


def classify_risk(score_0_100: float) -> tuple[str, str]:
    if score_0_100 < 25:
        return "LOW", "🟢"
    if score_0_100 < 50:
        return "MEDIUM", "🟡"
    if score_0_100 < 75:
        return "HIGH", "🟠"
    return "CRITICAL", "🔴"


model, meta = load_artifacts()

st.title("🦟 DengueGuard AI")
st.subheader("AI-Powered Urban Dengue Early Warning System (2–4 Week Lag Window)")
st.write(
    "Predicts ward-level dengue outbreak risk using multi-week weather lags "
    "and local urban vulnerability indicators."
)
st.divider()

if model is None or meta is None:
    st.error("Trained model not found. Run `python train.py` first to generate `models/dengue_model.pkl`.")
    st.stop()

ward_profiles: dict = meta["ward_profiles"]
ward_ids = sorted(ward_profiles.keys(), key=lambda x: int(x))

with st.sidebar:
    st.header("Control Panel")
    selected_ward = st.selectbox("Select Ward ID", options=ward_ids)
    profile = ward_profiles[selected_ward]
    st.caption(f"Location: {profile.get('city', 'Ward')} | Ward {selected_ward}")
    forecast_window = st.selectbox(
        "Early Warning Window",
        options=["2 Weeks (14-Day Lag)", "3 Weeks (21-Day Lag)", "4 Weeks (28-Day Lag)"],
        index=0,
    )
    st.caption(f"Chronological Test MAE: {meta['mae_14d']} | RMSE: {meta['rmse_14d']}")

st.header("Weather & Multi-Week Lag Inputs")
c1, c2, c3 = st.columns(3)
with c1:
    avg_temp = st.number_input("Avg Temperature (°C)", 10.0, 45.0, float(round(profile["avg_temp"], 2)))
    rain_7 = st.number_input("7-Day Lag Rainfall (mm)", 0.0, 2000.0, float(round(profile["rain_sum_7d"], 2)))
with c2:
    humidity = st.slider("Relative Humidity (%)", 10, 100, int(np.clip(round(profile["relative_hu"]), 10, 100)))
    rain_14 = st.number_input("14-Day Lag Rainfall (mm)", 0.0, 4000.0, float(round(profile["rain_sum_14d"], 2)))
with c3:
    rain_21 = st.number_input("21-Day Lag Rainfall (mm)", 0.0, 6000.0, float(round(profile["rain_sum_21d"], 2)))
    rain_28 = st.number_input("28-Day Lag Rainfall (mm)", 0.0, 8000.0, float(round(profile["rain_sum_28d"], 2)))

st.divider()
st.header("Ward Vulnerability Indicators")
v1, v2, v3 = st.columns(3)
with v1:
    water_logg = st.slider(
        "Water Logging Index",
        0.0,
        1.0,
        float(np.clip(profile["water_logg"], 0.0, 1.0)),
    )
with v2:
    population = st.number_input(
        "Population / Density Metric",
        0.0,
        5000000.0,
        float(max(profile["population"], 0.0)),
    )
with v3:
    sanitation = st.slider(
        "Sanitation Score",
        0.0,
        1.0 if profile["sanitation"] <= 1.0 else 100.0,
        float(profile["sanitation"]),
    )

st.divider()
st.header("Dengue Risk Analysis")

if st.button("Analyze Ward Risk", type="primary"):
    feature_row = {
        "population": float(population),
        "water_logg": float(water_logg),
        "sanitation": float(sanitation),
        "avg_temp": float(avg_temp),
        "rainfall_mr": float(profile["rainfall_mr"]),
        "relative_hu": float(humidity),
        "rain_sum_7d": float(rain_7),
        "rain_sum_14d": float(rain_14),
        "rain_sum_21d": float(rain_21),
        "rain_sum_28d": float(rain_28),
        "rain_mean_7d": float(rain_7 / 7.0),
        "rain_mean_14d": float(rain_14 / 14.0),
        "rain_mean_21d": float(rain_21 / 21.0),
        "rain_mean_28d": float(rain_28 / 28.0),
        "temp_mean_7d": float(avg_temp),
        "temp_mean_14d": float(avg_temp),
        "temp_mean_21d": float(avg_temp),
        "temp_mean_28d": float(avg_temp),
        "humidity_mean_7d": float(humidity),
        "humidity_mean_14d": float(humidity),
        "humidity_mean_21d": float(humidity),
        "humidity_mean_28d": float(humidity),
    }

    X_input = pd.DataFrame([feature_row])[meta["feature_cols"]]
    pred_cases = float(np.clip(model.predict(X_input)[0], 0.0, None))
    risk_score = float(np.clip((pred_cases / float(meta["risk_scale_cap"])) * 100.0, 0.0, 100.0))
    tier, icon = classify_risk(risk_score)

    m1, m2, m3 = st.columns(3)
    m1.metric("Risk Score", f"{risk_score:.1f} / 100")
    m2.metric("Risk Category", f"{icon} {tier}")
    m3.metric("Predicted 14-Day Cases", f"{pred_cases:.1f}")

    st.progress(int(np.clip(round(risk_score), 0, 100)))

    st.subheader("Key Drivers Breakdown")
    drivers_df = pd.DataFrame(
        {
            "Driver": [
                "14-Day Rainfall Lag (Breeding Window)",
                "21-Day Rainfall Lag (Incubation + Spread)",
                "Water Logging Index",
                "Relative Humidity (%)",
                "Avg Temperature (°C)",
            ],
            "Current Value": [
                f"{rain_14:.1f} mm",
                f"{rain_21:.1f} mm",
                f"{water_logg:.2f}",
                f"{humidity}%",
                f"{avg_temp:.1f} °C",
            ],
        }
    )
    st.dataframe(drivers_df, use_container_width=True, hide_index=True)

    st.subheader("Multi-Week Lagged Rainfall Trend")
    chart_data = pd.DataFrame(
        {
            "Lag Window": ["7-Day (1w)", "14-Day (2w)", "21-Day (3w)", "28-Day (4w)"],
            "Rainfall (mm)": [rain_7, rain_14, rain_21, rain_28],
        }
    )
    st.bar_chart(chart_data.set_index("Lag Window"))

    st.subheader("Recommended Public Health Actions")
    if tier in ("HIGH", "CRITICAL"):
        st.error("Prioritize stagnant water inspection, drain cleaning, and targeted vector control in this ward.")
    elif tier == "MEDIUM":
        st.warning("Increase ward-level surveillance, larvicide checks, and waste management.")
    else:
        st.success("Maintain routine vector surveillance and environmental hygiene.")

st.divider()
st.caption("DengueGuard AI | EDU AI Engineering Hackathon 2026 | Experimental decision-support prototype.")