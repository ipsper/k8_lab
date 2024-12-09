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

Applicera Kubernetes-manifesten:

```
kubectl apply -f postgres.yaml
kubectl apply -f fastapi.yaml
```

Få tillgång till applikationen: Kontrollera EXTERNAL-IP från kubectl get svc fastapi och använd den för att nå API:t.
