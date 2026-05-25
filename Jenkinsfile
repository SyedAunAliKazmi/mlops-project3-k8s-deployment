pipeline {
    agent any

    environment {
        // DagsHub Cloud Configuration - Replaces the local 127.0.0.1 server
        MLFLOW_TRACKING_URI      = "https://dagshub.com/kazmiaun032/mlops-project3.mlflow"
        MLFLOW_TRACKING_USERNAME = "kazmiaun032"
        MLFLOW_TRACKING_PASSWORD = "c80eaea30585653770fe829c28e2382a6cb81651"
        
        APP_NAME                 = "iris-mlops-app"
        NAMESPACE                = "mlops"
        KUBECONFIG               = "/var/lib/jenkins/.kube/config"
    }

    stages {
        stage('Checkout Repository') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/SyedAunAliKazmi/mlops-project3-k8s-deployment.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install --break-system-packages -r requirements.txt'
            }
        }

        stage('Cleanup Previous Run') {
            steps {
                sh '''
                    rm -f run_id.txt model_version.txt
                    echo "[CLEANUP] Done"
                '''
            }
        }

        stage('Data Ingestion') {
            steps {
                sh 'python3 src/data_ingest.py'
            }
        }

        stage('Model Training - MLflow') {
            steps {
                // The DagsHub credentials are automatically inherited from the environment block
                sh 'python3 src/train.py'
            }
        }

        stage('Model Evaluation') {
            steps {
                sh 'python3 src/evaluate.py'
            }
        }

        stage('Model Registration - MLflow Registry') {
            steps {
                sh 'python3 src/register_model.py'
            }
        }

        stage('Reload MLflow Wrapper') {
            steps {
                sh '''
                    echo "Reloading wrapper to pick up new Production model..."
                    systemctl restart mlflow-wrapper || true
                    sleep 10
                    echo "Wrapper reloaded"
                '''
            }
        }

        stage('ReplicaSet Deployment - Apply K8s Manifests') {
            steps {
                sh '''
                    echo "=== Applying Namespace ==="
                    kubectl apply -f k8s/namespace.yaml

                    echo "=== Applying Deployment (ReplicaSet x3) ==="
                    kubectl apply -f k8s/deployment.yaml

                    echo "=== Applying Service ==="
                    kubectl apply -f k8s/service.yaml

                    echo "=== Applying Nginx Ingress ==="
                    kubectl apply -f k8s/ingress.yaml

                    echo "=== Rolling Restart ==="
                    kubectl rollout restart deployment iris-mlops-app -n mlops
                    kubectl rollout status deployment iris-mlops-app -n mlops
                '''
            }
        }

        stage('Verify ReplicaSet Deployment') {
            steps {
                sh '''
                    echo "=== Pods ==="
                    kubectl get pods -n mlops

                    echo "=== ReplicaSet ==="
                    kubectl get replicaset -n mlops

                    echo "=== Services ==="
                    kubectl get services -n mlops

                    echo "=== Ingress (Nginx Load Balancer) ==="
                    kubectl get ingress -n mlops

                    echo "=== Pod Distribution ==="
                    kubectl describe pods -n mlops | grep -E "Node:|Name:|Status:"
                '''
            }
        }

        stage('Test API - K8s Endpoint') {
            steps {
                sh '''
                    sleep 15
                    echo "=== Health Check ==="
                    curl -s http://192.168.49.2:30007/health || echo "Health check failed."

                    echo "\\n=== Predict Setosa ==="
                    curl -s -X POST http://192.168.49.2:30007/predict \\
                        -H "Content-Type: application/json" \\
                        -d '{"features": [5.1, 3.5, 1.4, 0.2]}'

                    echo "\\n=== Predict Versicolor ==="
                    curl -s -X POST http://192.168.49.2:30007/predict \\
                        -H "Content-Type: application/json" \\
                        -d '{"features": [6.0, 2.9, 4.5, 1.5]}'

                    echo "\\n=== Predict Virginica ==="
                    curl -s -X POST http://192.168.49.2:30007/predict \\
                        -H "Content-Type: application/json" \\
                        -d '{"features": [6.7, 3.1, 5.6, 2.4]}'
                '''
            }
        }

        stage('Test MLflow Serving - Named Predictions') {
            steps {
                sh '''
                    echo "=== MLflow Tracking URI: https://dagshub.com/kazmiaun032/mlops-project3.mlflow ==="

                    echo "\\n--- Setosa ---"
                    curl -s -X POST http://127.0.0.1:7500/predict \\
                        -H "Content-Type: application/json" \\
                        -d '{"features": [5.1, 3.5, 1.4, 0.2]}' || echo "Wrapper service not responding"

                    echo "\\n--- Versicolor ---"
                    curl -s -X POST http://127.0.0.1:7500/predict \\
                        -H "Content-Type: application/json" \\
                        -d '{"features": [6.0, 2.9, 4.5, 1.5]}'

                    echo "\\n--- Virginica ---"
                    curl -s -X POST http://127.0.0.1:7500/predict \\
                        -H "Content-Type: application/json" \\
                        -d '{"features": [6.7, 3.1, 5.6, 2.4]}'
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline Successful — Syed Aun Ali Kazmi | SAP: 70149156 | BSES-A | 6th Semester | MLflow URI: https://dagshub.com/kazmiaun032/mlops-project3.mlflow"
        }
        failure {
            echo "Pipeline Failed — Check console output"
        }
    }
}
