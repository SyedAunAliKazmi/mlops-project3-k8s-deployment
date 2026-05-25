from flask import Flask, request, jsonify
from flask_cors import CORS
import mlflow.sklearn
import numpy as np

app = Flask(__name__)
CORS(app)

CLASS_NAMES = {0: "Setosa", 1: "Versicolor", 2: "Virginica"}
MODEL_PATH  = "/app/model_artifacts"
model       = None

def load_model():
    global model
    try:
        model = mlflow.sklearn.load_model(MODEL_PATH)
        print(f"[API] Model loaded from {MODEL_PATH}")
    except Exception as e:
        print(f"[API WARNING] Model load failed: {e}")
        model = None

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "project":  "MLOps Project 3 — K8s Cluster Deployment",
        "student":  "Syed Aun Ali Kazmi",
        "sap":      "70149156",
        "section":  "BSES-A",
        "semester": "6th",
        "endpoint": "/predict",
        "status":   "running"
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status":       "healthy",
        "model_loaded": model is not None
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    data = request.get_json()
    if not data or 'features' not in data:
        return jsonify({"error": "Missing 'features'", "format": {"features": [5.1, 3.5, 1.4, 0.2]}}), 400
    features = data['features']
    if len(features) != 4:
        return jsonify({"error": "Exactly 4 features required"}), 400
    arr   = np.array(features).reshape(1, -1)
    pred  = model.predict(arr)[0]
    proba = model.predict_proba(arr)[0].tolist()
    return jsonify({
        "prediction":    int(pred),
        "class_name":    CLASS_NAMES[int(pred)],
        "probabilities": {
            "Setosa":     round(proba[0], 4),
            "Versicolor": round(proba[1], 4),
            "Virginica":  round(proba[2], 4)
        },
        "input": {
            "sepal_length": features[0],
            "sepal_width":  features[1],
            "petal_length": features[2],
            "petal_width":  features[3]
        }
    })

if __name__ == '__main__':
    load_model()
    app.run(host='0.0.0.0', port=7000)
