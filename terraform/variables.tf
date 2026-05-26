variable "app_name" { default = "iris-mlops-app" }
variable "namespace" { default = "mlops" }
variable "replica_count" { default = 3 }
variable "app_port" { default = 7000 }
variable "image_name" { default = "aun12/iris-api:latest" }

variable "mlflow_uri" { default = "https://dagshub.com/kazmiaun032/mlops-project3.mlflow" }
variable "mlflow_username" { default = "kazmiaun032" }
variable "mlflow_password" { default = "c80eaea30585653770fe829c28e2382a6cb81651" }

variable "student_name" { default = "Syed-Aun-Ali-Kazmi" }
variable "sap_id" { default = "SAP-70149156" }
