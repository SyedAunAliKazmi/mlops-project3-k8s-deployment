pipeline {
    agent any

    environment {
        MLFLOW_TRACKING_URI = "http://localhost:5000"
        APP_NAME            = "iris-mlops-app"
        NAMESPACE           = "mlops"
        IMAGE_NAME          = "iris-api:latest"
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
                sh 'pip install -r requirements.txt'
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

        stage('Terraform Init') {
            steps {
                dir('terraform') {
                    sh 'terraform init'
                }
            }
        }

        stage('Terraform Plan') {
            steps {
                dir('terraform') {
                    sh 'terraform plan'
                }
            }
        }

        stage('Minikube Start + Build Docker Image') {
            steps {
                dir('terraform') {
                    sh 'terraform apply -target=null_resource.minikube_start -target=null_resource.build_image -auto-approve'
                }
            }
        }

        stage('Terraform Apply - K8s Deploy') {
            steps {
                dir('terraform') {
                    sh 'terraform apply -auto-approve'
                }
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
                    kubectl describe pods -n mlops | grep -E "Node:|Name:"
                '''
            }
        }

        stage('Test API Endpoint') {
            steps {
                sh '''
                    SERVICE_URL=$(minikube service iris-mlops-app-service -n mlops --url)
                    echo "Service URL: $SERVICE_URL"
                    curl -s $SERVICE_URL/health
                    curl -s -X POST $SERVICE_URL/predict \
                        -H "Content-Type: application/json" \
                        -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
                '''
            }
        }
    }

    post {
        success {
            echo "✅ K8s Deployment Pipeline Successful — Syed Aun Ali Kazmi | SAP: 70149156"
        }
        failure {
            echo "❌ Pipeline Failed — Check console output"
        }
    }
}
