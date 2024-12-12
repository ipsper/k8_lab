För att installera NGINX Ingress Controller i ditt Kubernetes-kluster kan du använda Helm, en populär pakethanterare för Kubernetes. Följ dessa steg:

1. Lägg till NGINX Ingress Controller Helm-repo:

```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
```

2. Installera NGINX Ingress Controller med Helm:

```
helm install nginx-ingress ingress-nginx/ingress-nginx

```

Detta kommando installerar NGINX Ingress Controller i ditt kluster med standardinställningar.

3. Verifiera installationen:

```
kubectl get pods -n default -l app.kubernetes.io/name=ingress-nginx
```

Du bör se NGINX Ingress Controller-poddar som körs i ditt kluster.
