variable "app_name" {
  description = "Application name"
  type        = string
  default     = "iris-mlops-app"
}

variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
  default     = "mlops"
}

variable "replica_count" {
  description = "Number of pod replicas (minimum 3)"
  type        = number
  default     = 3
}

variable "app_port" {
  description = "Flask API port"
  type        = number
  default     = 7000
}

variable "image_name" {
  description = "Docker image name"
  type        = string
  default     = "iris-api:latest"
}

variable "mlflow_uri" {
  description = "MLflow tracking URI"
  type        = string
  default     = "http://192.168.49.1:5000"
}

variable "student_name" {
  description = "Student name"
  type        = string
  default     = "Syed-Aun-Ali-Kazmi"
}

variable "sap_id" {
  description = "Student SAP ID"
  type        = string
  default     = "SAP-70149156"
}
