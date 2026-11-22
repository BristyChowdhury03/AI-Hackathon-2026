# DengueGuard AI – System Architecture

## 1. Project Overview
DengueGuard AI is an AI-powered dengue risk prediction system designed to analyze environmental and demographic factors and estimate potential dengue risk levels.

The system uses a machine learning model trained on a synthetic dataset to generate predictions based on user-provided input.

## 2. System Architecture

The system follows a modular architecture consisting of the following components:

### A. Presentation Layer
- Provides an interactive dashboard using Streamlit.
- Allows users to enter environmental data.
- Displays dengue risk prediction results.

### B. Processing Layer
- Handles user input.
- Validates and preprocesses the input data.
- Uses Python, Pandas, and NumPy for data processing.

### C. Machine Learning Layer
- Uses a trained machine learning model.
- Loads the saved model using Joblib.
- Analyzes environmental parameters to predict dengue risk.

### D. Data Layer
- Uses a synthetic CSV dataset for model training and testing.
- Stores environmental and demographic features.

## 3. Input Parameters

The system considers the following features:

1. Rainfall (mm)
2. Average Temperature (°C)
3. Relative Humidity (%)
4. Waterlogging Risk Index
5. Population Density (per sq. km)

## 4. Prediction Workflow

1. User opens the DengueGuard AI dashboard.
2. User provides environmental input values.
3. The system validates and preprocesses the input.
4. The trained machine learning model analyzes the data.
5. The system generates a dengue risk prediction.
6. Results are displayed on the dashboard.

## 5. Technology Stack

- **Programming Language:** Python
- **Frontend / Dashboard:** Streamlit
- **Data Processing:** Pandas, NumPy
- **Machine Learning:** Scikit-learn (if used for model training)
- **Model Serialization:** Joblib
- **Dataset Format:** CSV
- **Version Control:** Git and GitHub

## 6. Project Structure

```text
DengueGuard-AI/
│
├── app.py
├── train.py
├── models/
│   ├── dengue_model.pkl
│   └── model_meta.json
├── dataset/
│   └── dengue_dataset.csv
├── README.md
└── ARCHITECTURE.md
```

## 7. Dataset Description

The project uses a manually prepared synthetic environmental dataset for demonstration, testing, and machine learning development.

The dataset is not collected from any official government database or external real-world source.

## 8. Expected Output

The system aims to provide:
- Dengue risk level prediction.
- Environmental risk analysis.
- An interactive dashboard for presenting prediction results.
- Awareness and early risk identification support.

## 9. Future Improvements

- Integration of real-world weather data.
- Geographic dengue risk visualization.
- Larger datasets for improved model training.
- Real-time environmental monitoring.
- Deployment as a web-based application.
