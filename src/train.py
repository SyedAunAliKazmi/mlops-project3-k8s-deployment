import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import os

os.environ["MLFLOW_TRACKING_URI"] = "http://127.0.0.1:5000"
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
EXPERIMENT_NAME     = "iris-k8s-project3"

def train_model():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    iris = load_iris()
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    with mlflow.start_run() as run:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        acc = accuracy_score(y_test, model.predict(X_test))
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("random_state", 42)
        mlflow.log_metric("accuracy", acc)

        # Use artifact_path — works across all MLflow versions
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="iris-model",
            registered_model_name="iris-k8s-classifier"
        )
        print(f"[TRAIN] Accuracy: {acc} | Run ID: {run.info.run_id}")
        with open("run_id.txt", "w") as f:
            f.write(run.info.run_id)

if __name__ == "__main__":
    train_model()
