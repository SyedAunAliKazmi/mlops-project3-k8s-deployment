pipeline {
    agent any

    environment {
        MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
        APP_NAME            = "iris-mlops-app"
        NAMESPACE           = "mlops"
        IMAGE_NAME          = "iris-api:latest"
        MINIKUBE_IP         = "192.168.49.2"
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

        stage('Build Docker Image') {
            steps {
                sh '''
                    export DOCKER_TLS_VERIFY=$(minikube docker-env | grep DOCKER_TLS_VERIFY | cut -d= -f2 | tr -d '"')
                    export DOCKER_HOST=$(minikube docker-env | grep DOCKER_HOST | cut -d= -f2 | tr -d '"')
                    export DOCKER_CERT_PATH=$(minikube docker-env | grep DOCKER_CERT_PATH | cut -d= -f2 | tr -d '"')
                    export MINIKUBE_ACTIVE_DOCKERD=$(minikube docker-env | grep MINIKUBE_ACTIVE_DOCKERD | cut -d= -f2 | tr -d '"')
                    docker build -t iris-api:latest .
                '''
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

        stage('Terraform Apply - K8s Deploy') {
            steps {
                dir('terraform') {
                    sh 'terraform apply -auto-approve'
                }
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
                    sleep 15
                    curl -s http://192.168.49.2:30007/health
                    curl -s -X POST http://192.168.49.2:30007/predict \
                        -H "Content-Type: application/json" \
                        -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
                    curl -s -X POST http://192.168.49.2:30007/predict \
                        -H "Content-Type: application/json" \
                        -d '{"features": [6.0, 2.9, 4.5, 1.5]}'
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
