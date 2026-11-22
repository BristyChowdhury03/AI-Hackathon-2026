import streamlit as st
import pandas as pd

from dengue_prediction import predict_dengue_risk


# ==============================
# PAGE CONFIGURATION
# ==============================

st.set_page_config(
    page_title="DengueGuard AI",
    page_icon="🦟",
    layout="wide"
)


# ==============================
# CUSTOM DESIGN
# ==============================

st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
}

[data-testid="stMetric"] {
    background-color: #1c2330;
    padding: 18px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# ==============================
# DASHBOARD HEADER
# ==============================

st.title("🦟 DengueGuard AI")

st.subheader("Urban Dengue Risk Analysis Dashboard")

st.write(
    "Analyze potential dengue risk levels using "
    "weather and environmental indicators."
)

st.divider()


# ==============================
# SIDEBAR
# ==============================

st.sidebar.title("🏙️ Control Panel")

city = st.sidebar.selectbox(
    "Select City",
    ["Chattogram", "Dhaka"]
)

ward = st.sidebar.selectbox(
    "Select Ward",
    [f"Ward {i:02d}" for i in range(1, 42)]
)

prediction_window = st.sidebar.selectbox(
    "Prediction Window",
    ["2 Weeks", "3 Weeks", "4 Weeks"]
)

st.sidebar.info(
    "This dashboard uses a rule-based Dengue Risk Scoring Function."
)


# ==============================
# WEATHER DATA
# ==============================

st.header("🌦️ Weather & Environmental Data")

col1, col2, col3 = st.columns(3)

with col1:
    temperature = st.number_input(
        "Temperature (°C)",
        min_value=0.0,
        max_value=50.0,
        value=30.0
    )

with col2:
    humidity = st.slider(
        "Relative Humidity (%)",
        0, 100, 75
    )

with col3:
    rainfall = st.number_input(
        "Recent Rainfall (mm)",
        min_value=0.0,
        max_value=1000.0,
        value=50.0
    )


# ==============================
# MULTI-WEEK RAINFALL
# ==============================

st.subheader("🌧️ Multi-Week Rainfall History")

c1, c2, c3, c4 = st.columns(4)

with c1:
    rain_7 = st.number_input(
        "7-Day Rainfall (mm)",
        0.0, 2000.0, 40.0
    )

with c2:
    rain_14 = st.number_input(
        "14-Day Rainfall (mm)",
        0.0, 3000.0, 80.0
    )

with c3:
    rain_21 = st.number_input(
        "21-Day Rainfall (mm)",
        0.0, 4000.0, 120.0
    )

with c4:
    rain_28 = st.number_input(
        "28-Day Rainfall (mm)",
        0.0, 5000.0, 160.0
    )


st.divider()


# ==============================
# WARD VULNERABILITY
# ==============================

st.header("🏘️ Ward Vulnerability Indicators")

a, b, c = st.columns(3)

with a:
    water_logging = st.slider(
        "Water Logging Risk (%)",
        0, 100, 50
    )

with b:
    population_density = st.number_input(
        "Population Density (per sq km)",
        min_value=0,
        value=10000
    )

with c:
    sanitation = st.slider(
        "Sanitation Quality Score (0-100)",
        0, 100, 60
    )


st.divider()


# ==============================
# DENGUE RISK ANALYSIS
# ==============================

st.header("📊 Dengue Risk Analysis")


if st.button("Analyze Ward Risk", type="primary"):

    water_logging_score = water_logging / 10

    sanitation_score = sanitation / 10

    # Use the highest entered rainfall value
    prediction_rainfall = max(
        rainfall,
        rain_7,
        rain_14,
        rain_21,
        rain_28
    )

    # Call the prediction function
    risk_score, risk_level = predict_dengue_risk(
        rainfall=prediction_rainfall,
        temperature=temperature,
        humidity=humidity,
        water_logging_risk=water_logging_score,
        population_density=population_density,
        sanitation_score=sanitation_score
    )


    # ==============================
    # RISK RESULT
    # ==============================

    if risk_level == "Critical":
        risk_icon = "🔴"

    elif risk_level == "High":
        risk_icon = "🟠"

    elif risk_level == "Medium":
        risk_icon = "🟡"

    else:
        risk_icon = "🟢"


    st.subheader(f"Results: {ward}, {city}")

    x, y, z = st.columns(3)

    x.metric("Risk Score", f"{risk_score}/12")

    y.metric(
        "Risk Category",
        f"{risk_icon} {risk_level}"
    )

    z.metric(
        "Selected Window",
        prediction_window
    )

    st.progress(risk_score / 12)


    st.warning(
        "Prototype result: This is a rule-based risk score "
        "using sample data and predefined conditions. "
        "It is not a validated dengue outbreak prediction."
    )


    # ==============================
    # RAINFALL TREND CHART
    # ==============================

    st.subheader("📈 Rainfall Trend")

    chart_data = pd.DataFrame({
        "Period": [
            "7 Days",
            "14 Days",
            "21 Days",
            "28 Days"
        ],
        "Rainfall (mm)": [
            rain_7,
            rain_14,
            rain_21,
            rain_28
        ]
    })

    st.bar_chart(
        chart_data,
        x="Period",
        y="Rainfall (mm)"
    )


    # ==============================
    # RECOMMENDATIONS
    # ==============================

    st.subheader("🛡️ Recommended Actions")

    if risk_level in ["High", "Critical"]:

        st.error(
            "Increase environmental monitoring "
            "and inspect areas with stagnant water."
        )

        st.write(
            "- Inspect water-holding containers.\n"
            "- Improve waste collection.\n"
            "- Monitor vulnerable neighborhoods."
        )

    elif risk_level == "Medium":

        st.warning(
            "Increase ward-level monitoring "
            "and remove stagnant water."
        )

    else:

        st.success(
            "Continue routine mosquito prevention "
            "and environmental monitoring."
        )


# ==============================
# FOOTER
# ==============================

st.divider()

st.caption(
    "DengueGuard AI | EDU AI Engineering Hackathon 2026"
)

st.caption(
    "Experimental rule-based scoring system. "
    "Not intended for medical or public-health decisions."
)
