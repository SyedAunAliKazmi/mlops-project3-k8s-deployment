import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os
import sys

# DagsHub Cloud Configuration
os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/kazmiaun032/mlops-project3.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"] = "kazmiaun032"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "c80eaea30585653770fe829c28e2382a6cb81651"

MLFLOW_TRACKING_URI = os.environ["MLFLOW_TRACKING_URI"]
THRESHOLD           = 0.85

def evaluate_model():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    
    with open("run_id.txt") as f:
        run_id = f.read().strip()
        
    # Load model from DagsHub cloud
    model = mlflow.sklearn.load_model(f"runs:/{run_id}/iris-model")
    iris  = load_iris()
    _, X_test, _, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42)
        
    preds = model.predict(X_test)
    acc   = accuracy_score(y_test, preds)
    
    print(f"[EVALUATE] Accuracy: {acc}")
    print(classification_report(y_test, preds, target_names=iris.target_names))
    
    if acc < THRESHOLD:
        print(f"[EVALUATE] FAILED — below threshold {THRESHOLD}")
        sys.exit(1)
        
    print("[EVALUATE] PASSED")

if __name__ == "__main__":
    evaluate_model()
