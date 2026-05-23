import mlflow
from mlflow.tracking import MlflowClient
import os

os.environ["MLFLOW_TRACKING_URI"] = "http://127.0.0.1:5000"
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
MODEL_NAME          = "iris-k8s-classifier"

def register_model():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = MlflowClient()
    with open("run_id.txt") as f:
        run_id = f.read().strip()
    result  = mlflow.register_model(f"runs:/{run_id}/iris-model", MODEL_NAME)
    version = result.version
    print(f"[REGISTER] Model v{version} registered")
    client.set_registered_model_alias(MODEL_NAME, "Production", version)
    print(f"[REGISTER] Alias 'Production' set on v{version}")
    with open("model_version.txt", "w") as f:
        f.write(str(version))

if __name__ == "__main__":
    register_model()
