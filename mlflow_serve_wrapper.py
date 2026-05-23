"""
MLflow Model Wrapper API
Translates numeric predictions to Iris class names
Syed Aun Ali Kazmi | SAP: 70149156 | BSES-A | 6th Semester
MLflow Tracking URI: http://127.0.0.1:5000
"""

from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

MLFLOW_SERVING_URI = "http://127.0.0.1:6000/invocations"
CLASS_NAMES        = {0: "Setosa", 1: "Versicolor", 2: "Virginica"}
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "project":           "MLOps Project 3 — K8s Cluster Deployment",
        "student":           "Syed Aun Ali Kazmi",
        "mlflow_tracking":   MLFLOW_TRACKING_URI,
        "mlflow_serving":    MLFLOW_SERVING_URI,
        "predict_endpoint":  "/predict",
        "input_format":      {"features": [5.1, 3.5, 1.4, 0.2]}
    })

@app.route("/predict", methods=["POST"])
def predict():
    data     = request.get_json()
    features = data.get("features")
    if not features or len(features) != 4:
        return jsonify({"error": "Provide exactly 4 features: [sepal_length, sepal_width, petal_length, petal_width]"}), 400

    response = requests.post(
        MLFLOW_SERVING_URI,
        headers={"Content-Type": "application/json"},
        data=json.dumps({"inputs": [features]})
    )
    prediction_id = response.json()["predictions"][0]
    return jsonify({
        "mlflow_tracking_uri": MLFLOW_TRACKING_URI,
        "model":               "iris-k8s-classifier",
        "input": {
            "sepal_length": features[0],
            "sepal_width":  features[1],
            "petal_length": features[2],
            "petal_width":  features[3]
        },
        "prediction_id": prediction_id,
        "class_name":    CLASS_NAMES[prediction_id]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7500)
