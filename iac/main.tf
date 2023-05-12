terraform {
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "2.20.0"
    }
  }
}

provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "minikube"
}


resource "kubernetes_deployment" "example" {
  metadata {
    name = "exampletf"
    labels = {
      app = "exampletf"
    }
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "exampletf"
      }
    }

    template {
      metadata {
        labels = {
          app = "exampletf"
        }
      }

      spec {
        container {
          image = "nginx:latest"
          name = "exampletf"
          port {
            container_port = 80
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "example" {
  metadata {
    name = "exampletf"
  }

  spec {
    selector = {
      app = "exampletf"
    }

    port {
      port = 80
      target_port = 80
    }

    type = "LoadBalancer"
  }
}
