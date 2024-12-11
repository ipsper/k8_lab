# Här är ett exempel på en FastAPI-server som använder en PostgreSQL-databas och är redo att köras i Kubernetes. Exemplet inkluderar:

1. FastAPI-applikation med SQLAlchemy för databasanslutning.
2. Dockerfile för att paketera applikationen.
3. Kubernetes-manifest för att distribuera applikationen och databasen.

4. Bygga och distribuera
   Bygg Docker-bilden:

```
docker build -t your-dockerhub-username/fastapi-app:latest .
```

Pusha till Docker Hub:

```
docker push your-dockerhub-username/fastapi-app:latest

```

# Applicera Kubernetes-manifesten:

## install kind and

```
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

2. Create a kind Cluster
   Create a new Kubernetes cluster using kind:
   ￼
   kind create cluster

3. Apply the Configuration

```
kubectl apply -f kubernetes/postgres-secret.yaml
kubectl apply -f kubernetes/postgres-config.yaml
kubectl apply -f kubernetes/postgres-deployment.yaml
kubectl apply -f kubernetes/postgres-service.yaml
kubectl apply -f kubernetes/fastapi-deployment.yaml
kubectl apply -f kubernetes/fastapi-service.yaml

```

4. Verify the Deployment
   Check the status of your deployment and service:

```
kubectl get deployments
kubectl get services
```

5. Access the FastAPI Application
   Since kind runs inside Docker, you need to forward the port to access the FastAPI application from your host machine:

￼
kubectl port-forward service/fastapi 8080:80

Now, you can access your FastAPI application at http://localhost:8080.

6.  Clean Up
    When you are done, you can delete the kind cluster:

￼
kind delete cluster
This setup will deploy your FastAPI application in a kind Kubernetes cluster, connecting to a PostgreSQL database using the provided environment variable.

Få tillgång till applikationen: Kontrollera EXTERNAL-IP från kubectl get svc fastapi och använd den för att nå API:t.
