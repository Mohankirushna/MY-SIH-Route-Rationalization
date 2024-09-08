from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

model = joblib.load('My SIH\\model\\delay_predictor_model_1.joblib')

# Read the CSV file
def get_bus_schedule(bus_id):
    df = pd.read_csv('My SIH\\scheduling\\new_bus_schedule.csv')
    filtered_df = df[df['busid'] == bus_id]
    return filtered_df.to_dict(orient='records')

@app.route('/get_schedule', methods=['GET'])
def get_schedule():
    bus_id = int(request.args.get('bus_id'))
    schedule = get_bus_schedule(bus_id)
    return jsonify(schedule)

@app.route('/api/get_predicted_delay', methods=['POST'])
def get_predicted_duration():
    try:
        data = request.json
        print(f"Received data: {data}")  # Log received data
        features_dict = {
            'distance_meters': [data['distance_meters']],
            'duration_seconds': [data['duration_seconds']],
            'hour': [data['hour']],
            'day_of_week': [data['day_of_week']]
        }
        # features = np.array([[
        #     data['distance_meters'],
        #     data['duration_seconds'],
        #     data['duration_in_traffic_seconds'],
        #     data['hour'], 
        #     data['day_of_week']
        # ]])
        features_df = pd.DataFrame(features_dict)
        print(f"Features DataFrame: {features_df}")

        #print(f"Features: {features}, Shape: {features.shape}")  # Log features and shape

        # Predict using the model
        try:
            predicted_delay = model.predict(features_df)[0]
            predicted_delay = int(predicted_delay)  # Extract first value from prediction
        except Exception as e:
            print(f"Model prediction error: {str(e)}")
            return jsonify(error="Model prediction failed"), 500

        distance = data['distance_meters']
        actual_duration = data['duration_seconds']
        estimated_duration = data['duration_seconds'] + predicted_delay

        route_data = {
            "distance": distance,
            "actual_duration": actual_duration,
            "estimated_duration": estimated_duration,
            "predicted_delay": predicted_delay
        }

        # Return the prediction as JSON
        return jsonify(route_data)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify(error=str(e)), 400
# def get_predicted_duration():
#     try:
#         data = request.json
#         print(f"Received data: {data}")

#         features = np.array([[
#             data['distance_meters'],
#             data['duration_seconds'],
#             data['duration_in_traffic_seconds'],
#             data['hour'], 
#             data['day_of_week'], 
#         ]])
#         distance = data['distance']
#         estimated_duration = data['duration_in_traffic']
#         # Predict using the model
#         predicted_delay = model.predict(features)
#         route_data = {
#             "distance" : distance,
#             "estimated_duration": estimated_duration,
#             "predicted_delay": predicted_delay[0]
#         }
#         # Return the prediction as JSON
#         return jsonify(route_data)
    
#     except Exception as e:
#         return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True)
