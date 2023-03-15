# Add repo's
echo Adding repositories
helm repo add loki https://grafana.github.io/loki/charts
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts


# Install
echo Installing chart's
echo Installing chart's
helm upgrade
helm install loki grafana/loki-stack
helm install prometheus prometheus-community/prometheus
helm install grafana grafana/grafana

# Expose
echo Exposing services
kubectl expose service prometheus-server --type=NodePort --target-port=9090 --name=prometheus-server-np
kubectl expose service grafana --type=NodePort --target-port=3000 --name=grafana-np


