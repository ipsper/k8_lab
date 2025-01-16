# To deploy your FastAPI application using kind (Kubernetes IN Docker), follow these steps:

1. Install kind
   If you haven't installed kind yet, you can do so with the following command:

```
brew install kind
```

2. Create a kind Cluster
   Create a new Kubernetes cluster using kind:

```
kind create cluster
kind create cluster --config kubernetes/kind-config.yaml
```

3. Use cluster

Set kubectl context to "kind-kind"
You can now use your cluster with:

kubectl cluster-info --context kind-kind

Not sure what to do next? 😅 Check out https://kind.sigs.k8s.io/docs/user/quick-start/

```
kubectl cluster-info --context kind-kind
```

Kubernetes control plane is running at https://127.0.0.1:64831
CoreDNS is running at https://127.0.0.1:64831/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

```
kubectl cluster-info dump
```

### här slutar allt att funka

4. Apply the Configuration

- If Linux

```
  kubectl apply -f kubernetes/postgres-secret.yaml
  kubectl apply -f kubernetes/postgres-config.yaml
  kubectl apply -f kubernetes/postgres-deployment.yaml
  kubectl apply -f kubernetes/postgres-service.yaml
  kubectl apply -f kubernetes/fastapi-deployment.yaml
  kubectl apply -f kubernetes/fastapi-service.yaml
  kubectl apply -f kubernetes/fastapi-ingress.yaml
```

- If MacOs

```
  kubectl apply -f kubernetes/postgres-secret.yaml
  kubectl apply -f kubernetes/postgres-config.yaml
  kubectl apply -f kubernetes/postgres-deployment.yaml
  kubectl apply -f kubernetes/postgres-service.yaml
  kubectl apply -f kubernetes/fastapi-deployment-mac.yaml
  kubectl apply -f kubernetes/fastapi-service.yaml
  kubectl apply -f kubernetes/fastapi-ingress.yaml
```

5. Verify the Deployment
   Check the status of your deployment and service:

```
kubectl get deployments
kubectl get services
```

6. Installera NGINX Ingress Controller

Om EXTERNAL-IP för din tjänst är i tillståndet pending, kan det bero på att LoadBalancer-tjänsten inte kan allokera en extern IP-adress. Detta är vanligt i lokala Kubernetes-kluster som körs med kind eller minikube, eftersom de inte har en molnleverantör som tillhandahåller LoadBalancer-tjänster.

För att lösa detta kan du använda en Ingress Controller istället. Här är stegen för att konfigurera en Ingress Controller med kind:

- Installera NGINX Ingress Controller:

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

- Vänta tills alla pods är i Running-tillstånd:

```
kubectl get pods -n ingress-nginx --watch
```

Uppdatera din hosts-fil för att peka din domän till localhost:

```
sudo vi /etc/hosts
```

Lägg till följande rad:

127.0.0.1 your-domain.com
Byt ut your-domain.com med den domän du har angett i din Ingress-resurs.

- Testa din applikation genom att besöka http://your-domain.com i din webbläsare.
  Genom att använda en Ingress Controller kan du hantera trafik till din applikation utan att behöva en extern LoadBalancer.

6. Access the FastAPI Application
   Since kind runs inside Docker, you need to forward the port to access the FastAPI application from your host machine:

   Not needed if ingress is in use

```
kubectl port-forward service/fastapi 8080:80
```

1 vulnerability
hardcoded-credentials Embedding credentials in source code risks unauthorized access

Now, you can access your FastAPI application at
http://localhost:8080

7. Clean Up
   When you are done, you can delete the kind cluster:

```
kind delete cluster
```

This setup will deploy your FastAPI application in a kind Kubernetes cluster, connecting to a PostgreSQL database using the provided environment variable.
