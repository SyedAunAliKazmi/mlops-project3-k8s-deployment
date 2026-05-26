import mlflow
from mlflow.tracking import MlflowClient
import os

def transition_to_production():
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI"))
    client = MlflowClient()
    model_name = "iris-k8s-classifier"
    
    # Get the latest version
    latest_version = client.get_latest_versions(model_name, stages=["None"])[0].version
    
    # Transition to Production
    client.transition_model_version_stage(
        name=model_name,
        version=latest_version,
        stage="Production",
        archive_existing_versions=True
    )
    print(f"Successfully transitioned version {latest_version} to Production.")

if __name__ == "__main__":
    transition_to_production()
