resource "kubernetes_namespace" "mlops" {
  metadata {
    name = var.namespace
    labels = {
      project  = "mlops-project3"
      student  = var.student_name
      sap_id   = var.sap_id
      semester = "6th"
    }
  }
}

resource "kubernetes_deployment" "iris_api" {
  depends_on = [kubernetes_namespace.mlops]
  metadata {
    name      = var.app_name
    namespace = var.namespace
    labels    = { app = var.app_name }
  }
  spec {
    # REQUIREMENT 7.1: Explicitly set to 3 replicas for high availability
    replicas = 3 
    
    selector { match_labels = { app = var.app_name } }
    template {
      metadata { labels = { app = var.app_name } }
      spec {
        container {
          name              = "iris-api"
          image             = var.image_name
          image_pull_policy = "Always"

          port { container_port = var.app_port }

          # INSTRUCTOR REQUIREMENT: MLflow Tracking URI for cloud persistence
          env {
            name  = "MLFLOW_TRACKING_URI"
            value = "https://dagshub.com/kazmiaun032/mlops-project3.mlflow"
          }
          env {
            name  = "MLFLOW_TRACKING_USERNAME"
            value = "kazmiaun032"
          }
          env {
            name  = "MLFLOW_TRACKING_PASSWORD"
            value = "c80eaea30585653770fe829c28e2382a6cb81651"
          }

          resources {
            requests = { memory = "128Mi", cpu = "250m" }
            limits   = { memory = "256Mi", cpu = "500m" }
          }

          liveness_probe {
            http_get {
              path = "/health"
              port = var.app_port
            }
            initial_delay_seconds = 30
            period_seconds        = 10
          }

          readiness_probe {
            http_get {
              path = "/health"
              port = var.app_port
            }
            initial_delay_seconds = 5
            period_seconds        = 5
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "iris_api" {
  depends_on = [kubernetes_deployment.iris_api]
  metadata {
    name      = "${var.app_name}-service"
    namespace = var.namespace
  }
  spec {
    selector = { app = var.app_name }
    port {
      port        = 80
      target_port = var.app_port
      node_port   = 30007
    }
    type = "NodePort"
  }
}

# REQUIREMENT 7.9: Nginx Ingress for Load Balancing
resource "kubernetes_ingress_v1" "iris_api" {
  depends_on = [kubernetes_service.iris_api]
  metadata {
    name      = "${var.app_name}-ingress"
    namespace = var.namespace
    annotations = { "nginx.ingress.kubernetes.io/rewrite-target" = "/" }
  }
  spec {
    ingress_class_name = "nginx"
    rule {
      host = "iris-api.local"
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = "${var.app_name}-service"
              port { number = 80 }
            }
          }
        }
      }
    }
  }
}
