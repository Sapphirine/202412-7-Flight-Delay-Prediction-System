
# Flight Delay Prediction System

## Overview

Flight delays can significantly disrupt schedules and cause stress for travelers. To address this issue, we have developed a **Flight Delay Prediction System** that provides real-time and predictive delay estimates based on user input. Travelers can input their flight number, date, and destination to receive:

- **Predicted Arrival Delay**: Real-time estimates of arrival delays in minutes.
- **Flight Reliability Rating**: A letter grade (A to E) that summarizes the flight's likelihood of being on time.

Powered by machine learning, this system achieves an **R² score of 80%**, explaining 80% of the variance in delay times and ensuring predictions deviate from actual delays by no more than 20% on average.

---

## Features

- **Flight Delay Prediction**: Input flight details to predict arrival delay and reliability.
- **User-Friendly Interface**: Simple and intuitive web-based platform.
- **Real-Time and Predictive Insights**: Provides accurate delay estimates and grades for better planning.
- **High Accuracy**: Leveraging XGBoost Regressor with advanced preprocessing for reliable results.

---

## How It Works

1. **Input Flight Details**: Users enter their flight number, date, departure place, and destination.
2. **Data Processing**: The system matches input data with historical flight records, preprocesses features, and generates predictions using the trained machine learning model.
3. **Prediction and Rating**:
   - Predicts arrival delay in minutes.
   - Assigns a reliability grade (A to E) based on delay severity.

---

## Architecture

### Backend
- **Framework**: Flask for web application development.
- **Machine Learning Models**: XGBoost Regressor for delay prediction.
- **Data Handling**:
  - `pandas` for data manipulation.
  - `joblib` for model serialization and loading.

### Frontend
- Dynamic HTML templates to provide an interactive user experience.
- AJAX for real-time data fetching and updates.

### Data Pipeline
- **Data Preprocessing**:
  - Numerical features scaled using `StandardScaler`.
  - Categorical features encoded with `OneHotEncoder` and `LabelEncoder`.
  - Additional feature engineering for time-based patterns (e.g., sine and cosine transformations of departure times).
- **Model Training**:
  - Regression models: Linear Regression, Random Forest Regressor, XGBoost Regressor.
  - Model comparison based on MAE, MSE, RMSE, and R² scores.
  - Cross-validation to ensure robustness and generalization.

---

## Installation and Usage

### Prerequisites
- Python 3.8 or higher
- `pip` for dependency management

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/flight-delay-prediction.git
   cd flight-delay-prediction
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download required datasets and place them in the `./static/data/` folder:
   - `flights.csv`
   - `DeparturePlace.csv`
   - `ArrivalPlace.csv`

4. Ensure trained models (`XGBRegressor_AD_model.pkl`, `label_encoder.pkl`) are stored in `./static/models/`.

### Running the Application
1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

---

## Example Workflow

1. Enter flight details:
   - Flight number: `UA123`
   - Departure date: `2024-01-15`
   - Departure place: `San Francisco`
   - Destination: `Los Angeles`
2. Submit the form and view predictions:
   - **Predicted Arrival Delay**: `10 minutes`
   - **Reliability Rating**: `B`

---

## Results

### Model Performance
We compared three models during development:

| Model                  | MAE  | MSE   | RMSE  | R²    |
|------------------------|-------|-------|-------|-------|
| Linear Regression      | 5.86 | 56.69 | 7.53  | 0.79  |
| Random Forest Regressor| 6.13 | 61.19 | 7.82  | 0.78  |
| **XGBoost Regressor**  | **5.80** | **55.92** | **7.48** | **0.80** |

**XGBoost Regressor** was selected due to its superior performance across all metrics.

### Learning Curve
The learning curve shows that the XGBoost model achieves a balanced trade-off between bias and variance, ensuring robust predictions.

---

## Future Improvements

- **Hyperparameter Optimization**: Implement grid search or random search for model tuning.
- **Feature Importance Analysis**: Visualize key predictors of flight delays.
- **Enhanced Data Sources**: Integrate weather and airport traffic data for improved predictions.


