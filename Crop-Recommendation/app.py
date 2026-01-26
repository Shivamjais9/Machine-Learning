from flask import Flask, render_template, request
import numpy as np
import pickle

# Initialize Flask app
app = Flask(__name__)

# Load trained model
model = pickle.load(open('random_forest_model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])

        # Prediction
        prediction = model.predict(features)[0]

        # Confidence score
        proba = model.predict_proba(features)
        confidence = round(max(proba[0]) * 100, 2)

        return render_template(
            'index.html',
            prediction_text=f"Recommended Crop: {prediction}",
            confidence_text=f"Prediction Confidence: {confidence}%"
        )

    except Exception as e:
        return render_template(
            'index.html',
            prediction_text=f"Error: {str(e)}"
        )


if __name__ == '__main__':
    app.run(debug=True)
  