from flask import Flask, request, jsonify
import mlflow.pyfunc
import os
import time

app = Flask(__name__)

# Logic: Pull from DagsHub Cloud
MODEL_NAME = "iris-k8s-classifier"
STAGE = "Production"
TRACKING_URI = "https://dagshub.com/kazmiaun032/mlops-project3.mlflow"

mlflow.set_tracking_uri(TRACKING_URI)

model = None

def load_model():
    global model
    model_uri = f"models:/{MODEL_NAME}/{STAGE}"
    print(f"Attempting to load model from: {model_uri}")
    for i in range(5):  # Try 5 times
        try:
            model = mlflow.pyfunc.load_model(model_uri)
            print("Model loaded successfully!")
            return True
        except Exception as e:
            print(f"Attempt {i+1} failed: {e}")
            time.sleep(10)
    return False

# Initial load
load_model()

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        # Try one last time to load if it failed at startup
        if not load_model():
            return jsonify({"error": "Model not deployed yet. Check DagsHub Production stage."}), 503
    
    data = request.get_json()
    prediction = model.predict([data['features']])
    return jsonify({"prediction": int(prediction[0])})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model_loaded": model is not None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)
