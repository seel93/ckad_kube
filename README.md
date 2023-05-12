# Kubernetes init project

## Setup

### Cluster:

Init:
```bash
minikube start
```

Dashboard:

```bash
minikube dashboard
```

### Deployments:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: some-name-deployment
spec:
  selector:
    matchLabels:
      app: some-name
  replicas: 2
  template:
    metadata:
      labels:
        app: some-name
    spec:
      containers:
        - name: some-name
          image: some-name
          ports:
            - containerPort: 5000
          imagePullPolicy: Never
```
<hr>


### Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: some-service
spec:
  selector:
    app: some-app
  type: LoadBalancer 
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000
      nodePort: 32000
```

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$1
spec:
  rules:
  - host: example.com # remeber to set host in /etc/hosts locally!
    http:
      paths:
      - path: /backend/(.*)
        pathType: Prefix
        backend:
          service:
            name: servie-name
            port:
              number: 3000
```


### Mysql

Forward port for local connection:
```
kubectl port-forward service/mysql 3306:3306
```

establish connection with mysql-shell:
```
mysqlsh --uri=root@127.0.0.1:3306
```


### Outputs:

Get url 

```bash
k get service
minikube service <service_name> --url
```

### CI/CD:

<b>Updating image: </b>

run: 
```
eval (minikube docker-env)
```

and: 
```
docker build -t <img_name> .
```

### Cleanup:
Resetting the entire cluster:

```
minikube delete
```

### Observability:

<b> Sources: </b>
- prometheus
- grafana
- loki

Current [resource for prometheus and grafana](https://brain2life.hashnode.dev/prometheus-and-grafana-setup-in-minikube#heading-reference)
Current [resource for grafana and loki](https://medium.com/codex/setup-grafana-loki-on-local-k8s-cluster-minikube-90450e9896a8)

### Kafka:
Current [resource](https://redhat-developer-demos.github.io/kafka-tutorial/kafka-tutorial/1.0.x/07-kubernetes.html)



