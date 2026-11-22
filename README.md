# DengueGuard AI
### Urban Dengue Risk Analysis Dashboard

## 1. Project Overview

DengueGuard AI is a prototype project developed to analyze potential dengue risk levels using weather, environmental, and demographic indicators.

The project considers factors such as rainfall, temperature, relative humidity, waterlogging risk, population density, and sanitation score.

It processes the input data and assigns a potential risk category: Low, Medium, High, or Critical.

This project is developed as part of the **EDU AI Engineering Hackathon 2026**.

**Important:** The current system uses sample data and a predefined rule-based risk scoring method. It is an experimental prototype, not a medically validated dengue prediction or outbreak forecasting system.

## 2. Team Information

**Team Name:** Cerebral 3

### Team Members

| Name | Role |
|---|---|
| Bristy Chowdhury | Team Leader, Report & Repository Management |
| Arefin Mahmud Mahim | Dashboard Development |
| Fawjia Nasrin | Dengue Prediction |

## 3. Project Features

- Processes raw weather and environmental data.
- Performs feature engineering.
- Calculates potential dengue risk scores using predefined rules.
- Classifies risk levels into Low, Medium, High, and Critical.
- Provides interactive weather and environmental input fields.
- Displays ward-level risk results.
- Visualizes rainfall history using a chart.
- Provides risk-based environmental recommendations.

## 4. Project Structure

```text
Dengue Prediction/
│
├── data/
│   ├── raw_data.csv
│   ├── processed_data.csv
│   └── feature_data.csv
│
├── data_pipeline.py
├── feature_engineering.py
├── dengue_prediction.py
├── dashboard.py
└── README.md
```

## 5. Technology Stack

- Python 3
- Pandas
- NumPy
- Streamlit
- CSV

## 6. Setup and Run Instructions

### Requirements

- Python 3.x
- Visual Studio Code (recommended)

### Install Dependencies

Open a terminal in the project root directory and run:

```bash
python -m pip install pandas numpy streamlit
```

### Run the Data Pipeline

**Step 1: Process Raw Data**

```bash
python data_pipeline.py
```

**Step 2: Perform Feature Engineering**

```bash
python feature_engineering.py
```

**Step 3: Generate Dengue Risk Scores**

```bash
python dengue_prediction.py
```

**Step 4: Launch the Interactive Dashboard**

```bash
streamlit run dashboard.py
```

The dashboard will open in a browser, usually at:

```text
http://localhost:8501
```

## 7. Prediction Method

The current prototype uses a rule-based risk scoring approach.

Environmental and demographic indicators contribute to a predefined risk score. The total score is then classified into one of four categories:

- Low
- Medium
- High
- Critical

The scoring method uses predefined conditions rather than a trained machine learning model.

## 8. AI Tools and API Disclosure

- **AI Assistant:** ChatGPT (GPT-6) was used for programming guidance, debugging assistance, and documentation support.
- **AI Model Endpoint:** No external AI model endpoint is currently integrated into the application.
- **External APIs:** No external API is currently integrated into the prediction module.

## 9. Dataset and Attributions

- The project currently uses sample environmental and demographic records.
- The sample dataset is intended for demonstration and development.
- Python, Pandas, NumPy, and Streamlit are the technologies used in the project.
- ChatGPT was used for development guidance and documentation assistance.

## 10. Current Limitations

- The current dataset contains sample records and does not represent verified real-world dengue case data.
- The risk scoring method has not been clinically or epidemiologically validated.
- City and ward selections are currently used as dashboard labels and are not connected to verified geographic datasets.
- The prediction window is currently a display selection and does not perform validated future forecasting.
- Rainfall history and risk scoring logic require further improvement and validation.

## 11. Demo and Submission Links

- **GitHub Repository:** https://github.com/BristyChowdhury03/AI-Hackathon-2026
- **Project Demo Video:** Add Video Link
- **Live Demo:** Not currently deployed. The application can be run locally using the instructions above.

## 12. Important Disclaimer

DengueGuard AI is an experimental educational prototype. Its results are generated using sample data and predefined rules. They should not be interpreted as actual dengue forecasts, medical advice, or evidence of an outbreak.

Further development using reliable real-world data and proper validation is required before any real-world public-health application.