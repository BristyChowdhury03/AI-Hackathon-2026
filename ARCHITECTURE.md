
# DengueGuard AI - System Architecture

## 1. Project Overview

DengueGuard AI is an environmental risk analysis prototype designed to estimate potential dengue risk levels using weather and environmental indicators.

## 2. System Architecture

The project follows a step-by-step data processing workflow:

Raw Data (raw_data.csv)
        |
        v
Data Pipeline (data_pipeline.py)
        |
        v
Processed Data (processed_data.csv)
        |
        v
Feature Engineering (feature_engineering.py)
        |
        v
Feature Data (feature_data.csv)
        |
        v
Dengue Prediction (dengue_prediction.py)
        |
        v
Risk Score and Risk Level

The Streamlit dashboard (dashboard.py) provides an interactive interface for risk analysis.

## 3. Main Components

### A. Raw Dataset
- Contains sample environmental data.
- Includes rainfall, temperature, humidity, waterlogging risk, population density, and sanitation score.

### B. Data Pipeline
- Reads raw CSV data.
- Checks required columns and data validity.
- Sorts records by ward and week.
- Generates processed_data.csv.

### C. Feature Engineering
- Creates historical rainfall features.
- Generates four rainfall lag features.
- Saves the results in feature_data.csv.

### D. Dengue Prediction
- Uses a rule-based scoring method.
- Calculates risk scores from environmental indicators.
- Classifies risk into Low, Medium, High, and Critical.

### E. Dashboard
- Developed using Streamlit.
- Allows users to enter environmental information.
- Displays estimated risk scores, charts, and recommendations.

## 4. Technology Stack

- Python
- Pandas
- NumPy
- Streamlit
- CSV

## 5. Data Flow

1. Raw data is collected in raw_data.csv.
2. The data pipeline validates and processes the data.
3. Feature engineering creates historical rainfall features.
4. The prediction module calculates risk scores.
5. The dashboard displays the analysis results.

## 6. Current Limitations

- The dataset contains sample environmental records.
- Verified dengue case labels are not currently available.
- The system uses rule-based logic, not a trained machine learning model.
- Risk thresholds have not been scientifically validated.
- Results are experimental estimates, not confirmed outbreak predictions.

## 7. Future Improvements

- Integrate verified dengue case data.
- Use reliable weather datasets.
- Improve prediction logic through validation.
- Explore machine learning models with sufficient labeled data.
- Connect ward-level data with verified geographic information.

## 8. Disclaimer

DengueGuard AI is an educational prototype for environmental risk analysis. It is not a medical diagnostic tool or a validated dengue outbreak forecasting system.
