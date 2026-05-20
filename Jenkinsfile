pipeline {
    agent any

    environment {
        APP_NAME  = "iris-mlops-app"
        NAMESPACE = "mlops"
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
                    rm -f mlflow_pipeline.db run_id.txt model_version.txt
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

        stage('Verify Docker Image Exists') {
            steps {
                sh '''
                    IMAGE=$(sudo -u aun bash -c 'eval $(minikube docker-env) && docker images iris-api:latest --format "{{.Repository}}:{{.Tag}}"')
                    echo "Image found: $IMAGE"
                    if [ -z "$IMAGE" ]; then
                        echo "ERROR: iris-api:latest not found in Minikube"
                        exit 1
                    fi
                '''
            }
        }

        stage('Rollout Restart') {
            steps {
                sh '''
                    kubectl rollout restart deployment iris-mlops-app -n mlops
                    kubectl rollout status deployment iris-mlops-app -n mlops
                '''
            }
        }

        stage('Verify K8s Deployment') {
            steps {
                sh '''
                    echo "=== Pods ==="
                    kubectl get pods -n mlops

                    echo "=== ReplicaSet ==="
                    kubectl get replicaset -n mlops

                    echo "=== Services ==="
                    kubectl get services -n mlops

                    echo "=== Ingress ==="
                    kubectl get ingress -n mlops

                    echo "=== Pod Distribution ==="
                    kubectl describe pods -n mlops | grep -E "Node:|Name:|Status:"
                '''
            }
        }

        stage('Test API Endpoint') {
            steps {
                sh '''
                    sleep 20
                    echo "=== Health Check ==="
                    curl -s http://192.168.49.2:30007/health

                    echo "=== Predict Setosa ==="
                    curl -s -X POST http://192.168.49.2:30007/predict \
                        -H "Content-Type: application/json" \
                        -d '{"features": [5.1, 3.5, 1.4, 0.2]}'

                    echo "=== Predict Versicolor ==="
                    curl -s -X POST http://192.168.49.2:30007/predict \
                        -H "Content-Type: application/json" \
                        -d '{"features": [6.0, 2.9, 4.5, 1.5]}'

                    echo "=== Predict Virginica ==="
                    curl -s -X POST http://192.168.49.2:30007/predict \
                        -H "Content-Type: application/json" \
                        -d '{"features": [6.7, 3.1, 5.6, 2.4]}'
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline Successful — Syed Aun Ali Kazmi | SAP: 70149156 | BSES-A | 6th Semester"
        }
        failure {
            echo "Pipeline Failed — Check console output"
        }
    }
}
