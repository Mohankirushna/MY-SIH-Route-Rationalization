from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Loading
model = joblib.load('My SIH\\model\\delay_predictor_model.joblib')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_predicted_delay', methods=['POST'])
def get_predicted_duration():
    try:
        data = request.json
        features = np.array([[
            data['hour'], 
            data['day_of_week'], 
            data['distance'],
            data['duration'], 
            data['duration_in_traffic']
        ]])
        
        # Predict using the model
        predicted_delay = model.predict(features)
        
        # Return the prediction as JSON
        return jsonify(predicted_duration=predicted_delay[0])
    
    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True)
