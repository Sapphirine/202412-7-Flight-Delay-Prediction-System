from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import numpy as np


app = Flask(__name__)

# Load flight data
FLIGHT_DATA_PATH = './static/data/flights.csv'
flights_df = pd.read_csv(FLIGHT_DATA_PATH)
print("Flight data loaded successfully.")

# Load the models
MODEL_PATH = './static/models/XGBRegressor_AD_model.pkl'
LABEL_ENCODER_PATH = './static/models/label_encoder.pkl'

prediction_model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(LABEL_ENCODER_PATH)
print("Models and label encoder loaded successfully.")

# Load departure and arrival places
DEPARTURE_PLACES_PATH = './static/data/DeparturePlace.csv'
ARRIVAL_PLACES_PATH = './static/data/ArrivalPlace.csv'

departure_places = pd.read_csv(DEPARTURE_PLACES_PATH)['place'].tolist()
arrival_places = pd.read_csv(ARRIVAL_PLACES_PATH)['place'].tolist()
print('Departure and arrival places load succeed.')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_places', methods=['GET'])
def get_places():
    place_type = request.args.get('type')
    if place_type == 'departure':
        return jsonify(departure_places)
    elif place_type == 'arrival':
        return jsonify(arrival_places)
    return jsonify({'error': 'Invalid place type'}), 400

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract user inputs
        user_flight_number = request.json.get('flight_number')
        user_date = request.json.get('departure_date')
        user_departure_place = request.json.get('departure_place')
        user_arrival_place = request.json.get('arrival_place')

        print('Inputs extracted successfully!')

        # Match the row in the dataset
        year, month, day = map(int, user_date.split('-'))
        matched_row = flights_df[
            (flights_df['flight_code'] == user_flight_number) &
            (flights_df['YEAR'] == year) &
            (flights_df['MONTH'] == month) &
            (flights_df['DAY_OF_MONTH'] == day) &
            (flights_df['ORIGIN_CITY_NAME'] == user_departure_place) &
            (flights_df['DEST_CITY_NAME'] == user_arrival_place)
        ]
        print('Row matched successfully!')
        print('matched row:', matched_row)
        print(1)
        
        if matched_row.empty:
            return jsonify({'error': 'No flight found for the given inputs.'}), 404

        print(2)
        print("type of matched_row['CRS_DEP_TIME'].values[0]: ", matched_row['CRS_DEP_TIME'].values[0])
        scheduled_departure_time = int(matched_row['CRS_DEP_TIME'].values[0])
        print("scheduled_departure_time: ", scheduled_departure_time)
        dep_hour = scheduled_departure_time // 100  # Extract hours
        dep_minute = scheduled_departure_time % 100  # Extract minutes
        departure_time_formatted = f"{dep_hour:02}:{dep_minute:02}"
        print('Departure time scheduled: ', departure_time_formatted)

        # Format scheduled arrival time (CRS_ARR_TIME)
        scheduled_arrival_time = int(matched_row['CRS_ARR_TIME'].values[0])
        arr_hour = scheduled_arrival_time // 100  # Extract hours
        arr_minute = scheduled_arrival_time % 100  # Extract minutes
        arrival_time_formatted = f"{arr_hour:02}:{arr_minute:02}"
        print('Arrival time scheduled', arrival_time_formatted)


        # Extract required features for the model
        required_features = [
            "MKT_UNIQUE_CARRIER", "ORIGIN_CITY_NAME", "DEST_CITY_NAME",
            "DEP_DELAY", "DISTANCE", "Day", "DepTime_sin", "DepTime_cos"
        ]

        prediction_row = matched_row[required_features]
        print("Prediction row type: ", type(prediction_row))  # DataFrame
        print('Prediction row:', prediction_row)

        # Convert the prediction row into the correct format for the model
        prediction_features = prediction_row.values
        print('Prediction features type: ', type(prediction_features))  # numpy.ndarray
        print('Prediction features shape: ', prediction_features.shape)  # (1,8)

        # Predict the arrival delay
        predicted_arrival_delay = prediction_model.predict(prediction_row)[0]
        print(1)
        predicted_arr_delay_int = int(predicted_arrival_delay)
        print('Predicted Arrival Delay:', predicted_arrival_delay, 'Predictions made successfully!')

        # Calculate the ranking based on the predicted arrival delay
        if predicted_arr_delay_int <= -20:
            ranking = 'A'
        elif -19 <= predicted_arrival_delay <= 0:
            ranking = 'B'
        elif 1 <= predicted_arrival_delay <= 10:
            ranking = 'C'
        elif 11 <= predicted_arrival_delay <= 20:
            ranking = 'D'
        else: # predicted_arrival_delay >= 20
            ranking = 'E'
        
        flight_delay = int(matched_row['DEP_DELAY'].values[0]) - predicted_arr_delay_int

        # Prepare response data
        response = {
            'flight_number': str(matched_row['flight_code'].values[0]),
            'airline': str(matched_row['MKT_UNIQUE_CARRIER'].values[0]),
            'airplane': str(matched_row['MKT_CARRIER_FL_NUM'].values[0]),
            'departure_time': departure_time_formatted,  # Use the combined time frame
            'arrival_time': arrival_time_formatted,
            'origin': str(matched_row['ORIGIN_CITY_NAME'].values[0]),
            'destination': str(matched_row['DEST_CITY_NAME'].values[0]),
            'ranking': ranking,
            'predicted_arrival_delay': int(predicted_arrival_delay),
            'flight_delay': flight_delay
        }

        return jsonify(response)

    except Exception as e:
        print(f"Error occurred: {e}")
        # If an error occurs, return basic flight info and an error message
        if not matched_row.empty:
            response = {
                'flight_number': str(matched_row['flight_code'].values[0]),
                'airline': str(matched_row['MKT_UNIQUE_CARRIER'].values[0]),
                'airplane': str(matched_row['MKT_CARRIER_FL_NUM'].values[0]),
                'departure_time': departure_time_formatted,
                'arrival_time': arrival_time_formatted,
                'origin': str(matched_row['ORIGIN_CITY_NAME'].values[0]),
                'destination': str(matched_row['DEST_CITY_NAME'].values[0]),
                'ranking': 'not available',
                'predicted_arrival_delay': 'not available'
            }
            return jsonify(response), 500

        return jsonify({'error': 'An error occurred while processing the request.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
