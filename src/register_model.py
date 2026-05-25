import mlflow
from mlflow.tracking import MlflowClient
import os

# DagsHub Cloud Configuration
os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/kazmiaun032/mlops-project3.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"] = "kazmiaun032"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "c80eaea30585653770fe829c28e2382a6cb81651"

MLFLOW_TRACKING_URI = os.environ["MLFLOW_TRACKING_URI"]
MODEL_NAME          = "iris-k8s-classifier"

def register_model():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = MlflowClient()
    
    with open("run_id.txt") as f:
        run_id = f.read().strip()

    # Get latest version just registered on DagsHub
    versions = client.get_latest_versions(MODEL_NAME)
    if versions:
        version = versions[-1].version
    else:
        result  = mlflow.register_model(f"runs:/{run_id}/iris-model", MODEL_NAME)
        version = result.version

    print(f"[REGISTER] Model v{version} found on DagsHub")
    client.set_registered_model_alias(MODEL_NAME, "Production", version)
    print(f"[REGISTER] Alias 'Production' set on v{version}")
    
    with open("model_version.txt", "w") as f:
        f.write(str(version))

if __name__ == "__main__":
    register_model()
