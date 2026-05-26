from flask import Flask, request, jsonify
from flask_cors import CORS
import mlflow.sklearn
import os

app = Flask(__name__)
CORS(app)

# Load from Registry Alias
MODEL_URI = "models:/iris-k8s-classifier/Production"
model = None

def load_production_model():
    global model
    try:
        mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI"))
        model = mlflow.sklearn.load_model(MODEL_URI)
        print("[API] Production model loaded successfully.")
    except Exception as e:
        print(f"[API ERROR] Failed to pull model: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    if not model: return jsonify({"error": "Model not ready"}), 503
    data = request.json['features']
    prediction = model.predict([data])
    return jsonify({"prediction": int(prediction[0])})

@app.route('/health')
def health(): return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    load_production_model()
    app.run(host='0.0.0.0', port=7000)
