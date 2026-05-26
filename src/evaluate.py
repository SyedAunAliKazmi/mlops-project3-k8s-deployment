import mlflow
import mlflow.sklearn
import os, time

def evaluate_model():
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI"))
    with open("run_id.txt", "r") as f:
        run_id = f.read().strip()

    # CRITICAL: Path must be "model" to match train.py
    model_uri = f"runs:/{run_id}/model"
    
    # Socratic Fix: Retry loop to handle DagsHub sync latency
    for i in range(3):
        try:
            model = mlflow.sklearn.load_model(model_uri)
            print("[EVAL] Model loaded successfully.")
            return
        except Exception as e:
            print(f"[EVAL] Syncing from DagsHub... Attempt {i+1}/3")
            time.sleep(15)
    raise Exception("Artifact not found after retries.")

if __name__ == "__main__":
    evaluate_model()
