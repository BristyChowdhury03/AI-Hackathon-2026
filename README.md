# DengueGuard-AI

## 1. Title & Description
**DengueGuard-AI** is a dengue risk prediction and interactive analytics dashboard built for the AI Hackathon (`AI-Hackathon-2026`). It addresses early dengue screening and risk awareness by combining a trained machine learning model (`models/dengue_model.pkl` and `models/model_meta.json`), training pipeline (`train.py`), dataset, and a Streamlit web interface (`app.py`).

## 2. Team
- **Team Name:** Cerebral 3
- **Members & Roles:**
  - **Samiya Karim Bristy** (`BristyChowdhury03`) — Team Leader & GitHub / Repository Management
  - **Fawzia Nasrin** (`marwausa`) — ML Model Development
  - **Arefin Mahmud Mahim** (`arefinmahmudmahim0-crypto`) — Streamlit Dashboard (`app.py`) & Application Integration

## 3. Tech Stack
- **Language:** Python
- **Web / Dashboard Framework:** Streamlit (`app.py`)
- **Data & ML Libraries:** `pandas`, `numpy`, `joblib`, plus packages listed in `requirements.txt`
- **Model & Metadata Artifacts:** `models/dengue_model.pkl`, `models/model_meta.json`
- **Version Control & Hosting:** Git & GitHub (`AI-Hackathon-2026`)
## 4. Setup & Run Instructions
1. Clone or open the repository (`AI-Hackathon-2026`) and navigate to the project directory (`D:\DengueGuard-AI` if running locally).
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
 ### 3. Run the Streamlit Application

```bash
streamlit run app.py
```

4. Open the Dashboard

After running the command, open the local URL displayed in the terminal to access the dashboard.

5. AI Tools & APIs Disclosure

Machine Learning: A trained ML model is used for dengue risk prediction.

AI Assistants: ChatGPT (OpenAI) was used for documentation, coding guidance, and troubleshooting during development.

External APIs: None. The application uses a trained machine learning model for prediction.

6. Attributions

**Dataset Source:** Self-created synthetic sample dataset for the DengueGuard AI project. It was manually prepared for testing and demonstrating the dengue risk prediction system. It is not collected from any official government or external database.

**Dataset Features:**
1. Rainfall (mm)
2. Average Temperature (°C)
3. Relative Humidity (%)
4. Waterlogging Risk Index
5. Population Density (per sq. km)
6. Sanitation Score

**Dataset License:** No external dataset license applies because the dataset was self-created using synthetic sample data. The project team should specify a license for the dataset if required for distribution.

7. Demo Link

Live Demo: Not deployed yet

Demo Video: To be added.

Local Demo: Run the application using the instructions above.

Developed by Team Cerebral 3

AI Hackathon 2026
