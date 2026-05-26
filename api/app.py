from flask import Flask, request, jsonify
import mlflow.sklearn
import os

app = Flask(__name__)

# Registry alias for Production (Fulfills PDF Task 5.2)
MODEL_URI = "models:/iris-k8s-classifier@Production"
model = None

def load_model():
    global model
    try:
        mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI"))
        model = mlflow.sklearn.load_model(MODEL_URI)
        print("[API] Successfully loaded Production model from DagsHub!")
    except Exception as e:
        print(f"[API ERROR] Model not found yet. Awaiting Jenkins pipeline run. Error: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    if model is None: 
        return jsonify({"error": "Model not deployed yet."}), 503
    data = request.json.get('features')
    prediction = model.predict([data])
    return jsonify({"prediction": int(prediction[0])})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "model_ready": model is not None}), 200

if __name__ == '__main__':
    load_model()
    app.run(host='0.0.0.0', port=7000)
