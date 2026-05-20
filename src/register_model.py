import mlflow
from mlflow.tracking import MlflowClient

MLFLOW_URI = "sqlite:///mlflow_local.db"
MODEL_NAME = "iris-k8s-classifier"

def register_model():
    mlflow.set_tracking_uri(MLFLOW_URI)
    client = MlflowClient()
    with open("run_id.txt") as f:
        run_id = f.read().strip()
    result  = mlflow.register_model(f"runs:/{run_id}/model", MODEL_NAME)
    version = result.version
    client.set_registered_model_alias(MODEL_NAME, "Production", version)
    print(f"[REGISTER] Model v{version} registered as 'Production'")
    with open("model_version.txt", "w") as f:
        f.write(str(version))

if __name__ == "__main__":
    register_model()
