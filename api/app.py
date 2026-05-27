from flask import Flask, request, jsonify
import mlflow.pyfunc
import os
import time

app = Flask(__name__)

# Iris Species Mapping Logic
SPECIES_MAP = {0: "setosa", 1: "versicolor", 2: "virginica"}

# Logic: Pull from DagsHub Cloud for WSL-off persistence
MODEL_NAME = "iris-k8s-classifier"
STAGE = "Production"
TRACKING_URI = "https://dagshub.com/kazmiaun032/mlops-project3.mlflow"

mlflow.set_tracking_uri(TRACKING_URI)
model = None

def load_model():
    global model
    model_uri = f"models:/{MODEL_NAME}/{STAGE}"
    for i in range(5):
        try:
            model = mlflow.pyfunc.load_model(model_uri)
            return True
        except Exception as e:
            print(f"Load attempt {i+1} failed. Retrying...")
            time.sleep(10)
    return False

load_model()

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        if not load_model():
            return jsonify({"error": "Model not deployed"}), 503
    
    data = request.get_json()
    prediction_int = int(model.predict([data['features']])[0])
    
    # Socratic Fix: Map integer to Name
    species_name = SPECIES_MAP.get(prediction_int, "unknown")
    
    return jsonify({
        "prediction_index": prediction_int,
        "species": species_name
    })

@app.route('/health', netthods=['GET'])
def health():
    return jsonify({"status": "healthy", "model_loaded": model is not None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)
