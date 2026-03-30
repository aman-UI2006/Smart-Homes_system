# -------------------------------
# 1. Imports
# -------------------------------
import os
from pathlib import Path

import mysql.connector
from flask import Flask, request, jsonify
import numpy as np
from flask_cors import CORS
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from dotenv import load_dotenv
from groq import Groq

load_dotenv(Path(__file__).resolve().parent / ".env")
client = Groq(api_key=os.getenv("GROQ_API_KEY") or "")


# -------------------------------
# 2. Create Flask App
# -------------------------------
app = Flask(__name__)
CORS(app)


# -------------------------------
# 3. Database Connection (optional — app runs without MySQL)
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent
db = None
cursor = None
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aman@2006",
        database="smart_energy",
    )
    cursor = db.cursor()
except mysql.connector.Error:
    pass


# -------------------------------
# 4. Load Model + Scaler
# -------------------------------
CSV_PATH = BASE_DIR / "AEP_hourly.csv"
MODEL_PATH = BASE_DIR / "lstm_model.h5"

df = pd.read_csv(CSV_PATH)
data = df["AEP_MW"].values.reshape(-1, 1)

scaler = MinMaxScaler()
scaler.fit(data)

model = None
if MODEL_PATH.exists():
    print("Model loaded successfully")
    model = load_model(str(MODEL_PATH), compile=False)


def get_ai_suggestion(prediction, appliance_data):
    try:
        if not os.getenv("GROQ_API_KEY"):
            return "AI suggestion unavailable: add GROQ_API_KEY to .env"

        if isinstance(appliance_data, dict) and appliance_data:
            lines = "\n".join(f"- {k}: {v} kWh" for k, v in appliance_data.items())
        else:
            lines = str(appliance_data) if appliance_data else "(no appliance breakdown provided)"

        prompt = f"""
You are a smart home energy optimization AI.

Energy prediction: {prediction} MW

Appliance usage:
{lines}

Analyze and return:

1. Total consumption insight
2. Which appliance consumes most energy
3. Wastage detection
4. Practical suggestions to reduce energy
5. Cost saving tips

Be specific. Mention appliances like AC, fridge, etc.
Keep answer short and actionable.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {str(e)}"


# -------------------------------
# 5. Routes
# -------------------------------

@app.route('/')
def home():
    return "Smart Energy API — ready"


def _predict_mw(raw_input) -> float:
    arr = np.array(raw_input, dtype=float).reshape(-1, 1)
    input_scaled = scaler.transform(arr).reshape(1, 24, 1)
    if model is not None:
        pred_scaled = model.predict(input_scaled, verbose=0)
        return float(scaler.inverse_transform(pred_scaled)[0][0])
    return float(np.mean(arr))


# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        body = request.get_json(silent=True) or {}
        print("Incoming request:", body)
        print("Headers:", request.headers)
        input_data = body.get("input")
        if input_data is None:
            return jsonify({"error": "Missing 'input'"}), 400

        input_data = np.array(input_data, dtype=float).reshape(1, -1)
        print("Model input:", input_data)
        print("Input shape:", input_data.shape)

        pred_actual = _predict_mw(input_data)
        pred_actual = float(pred_actual)

        print("Prediction result:", pred_actual)

        return jsonify({
            'prediction_MW': pred_actual
        })

    except Exception as e:
        print(f"Error in /predict: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/optimize', methods=['POST'])
def optimize():
    try:
        body = request.get_json(silent=True) or {}
        print("Incoming request:", body)
        print("Headers:", request.headers)
        input_data = body.get("input")
        if input_data is None:
            return jsonify({"error": "Missing 'input'"}), 400

        appliance_data = body.get("appliances") or {}

        input_data = np.array(input_data, dtype=float).reshape(1, -1)
        print("Model input:", input_data)
        print("Input shape:", input_data.shape)

        pred_actual = _predict_mw(input_data)
        pred_actual = float(pred_actual)

        if pred_actual < 14000:
            status = "Low usage"
            suggestion = "Energy usage is optimal. No action needed."
        elif 14000 <= pred_actual < 15500:
            status = "Moderate usage"
            suggestion = "Try reducing non-essential appliances during peak hours."
        else:
            status = "High usage"
            suggestion = "Reduce AC/heater usage and shift heavy loads to off-peak hours."

        ai_suggestion = get_ai_suggestion(pred_actual, appliance_data)

        # Persist to database
        query = """
        INSERT INTO predictions (input_data, prediction, status, suggestion)
        VALUES (%s, %s, %s, %s)
        """

        values = (
            str(input_data.tolist()),
            float(pred_actual),
            status,
            suggestion
        )

        if cursor is not None and db is not None:
            try:
                cursor.execute(query, values)
                db.commit()
            except mysql.connector.Error:
                pass

        print("Prediction result:", pred_actual)
        
        return jsonify({
            'prediction_MW': float(pred_actual),
            'status': status,
            'suggestion': suggestion,
            'ai_suggestion': ai_suggestion,
        })

    except Exception as e:
        print(f"Error in /optimize: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/history', methods=['GET'])
def history():
    if cursor is None:
        return jsonify([])
    cursor.execute("SELECT * FROM predictions ORDER BY created_at DESC LIMIT 10")
    rows = cursor.fetchall()

    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "input_data": row[1],
            "prediction": row[2],
            "status": row[3],
            "suggestion": row[4],
            "time": str(row[5])
        })

    return jsonify(data)


# -------------------------------
# 6. Run App
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)