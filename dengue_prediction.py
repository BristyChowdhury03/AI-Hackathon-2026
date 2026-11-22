
import pandas as pd


def predict_dengue_risk(
    rainfall,
    temperature,
    humidity,
    water_logging_risk,
    population_density,
    sanitation_score
):
    risk_score = 0

    # Rainfall risk
    if rainfall >= 200:
        risk_score += 3
    elif rainfall >= 100:
        risk_score += 2
    elif rainfall >= 50:
        risk_score += 1

    # Temperature risk
    if temperature >= 30:
        risk_score += 2
    elif temperature >= 25:
        risk_score += 1

    # Humidity risk
    if humidity >= 80:
        risk_score += 2
    elif humidity >= 60:
        risk_score += 1

    # Waterlogging risk: supports both 0-1 and 0-10 scales
    if water_logging_risk <= 1:
        waterlogging_value = water_logging_risk
        waterlogging_threshold = 0.7
    else:
        waterlogging_value = water_logging_risk
        waterlogging_threshold = 7

    if waterlogging_value >= waterlogging_threshold:
        risk_score += 2

    # Population density
    if population_density >= 10000:
        risk_score += 1

    # Sanitation score
    if sanitation_score <= 3:
        risk_score += 2

    # Risk category
    if risk_score >= 9:
        risk_level = "Critical"
    elif risk_score >= 6:
        risk_level = "High"
    elif risk_score >= 3:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return risk_score, risk_level


if __name__ == "__main__":

    data = pd.read_csv("data/feature_data.csv")

    for index, row in data.iterrows():

        score, level = predict_dengue_risk(
            row["rainfall_mm"],
            row["avg_temp_C"],
            row["relative_humidity_pct"],
            row["water_logging_risk_index"],
            row["population_density_sqkm"],
            row["sanitation_score"]
        )

        print("Ward:", int(row["ward_id"]))
        print("Risk Score:", score)
        print("Risk Level:", level)
        print("----------------------")
