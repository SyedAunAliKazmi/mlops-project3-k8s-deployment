import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os

def train_model():
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI"))
    mlflow.set_experiment("iris-k8s-project3")
    
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2)

    with mlflow.start_run() as run:
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        
        # We use "model" as the path, and register it immediately
        mlflow.sklearn.log_model(
            sk_model=model, 
            artifact_path="model", 
            registered_model_name="iris-k8s-classifier"
        )
        
        with open("run_id.txt", "w") as f:
            f.write(run.info.run_id)
        print(f"[TRAIN] Run ID: {run.info.run_id}")

if __name__ == "__main__":
    train_model()
