import mlflow
from mlflow.tracking import MlflowClient
import os

def register():
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI"))
    client = MlflowClient()
    model_name = "iris-k8s-classifier"
    
    # Get latest version that was just trained
    versions = client.get_latest_versions(model_name, stages=["None"])
    latest = versions[0].version
    
    # Transition to Production
    client.transition_model_version_stage(
        name=model_name,
        version=latest,
        stage="Production",
        archive_existing_versions=True
    )
    print(f"[REGISTRY] Version {latest} is now PRODUCTION.")

if __name__ == "__main__":
    register()
