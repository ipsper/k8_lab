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

# lite debug

1. Check Pod Status
   Check the status of the pods to get more details:

```
kubectl get pods
```

1. 1. Check All Namespaces

```
kubectl get pods --all-namespaces
```

2. Describe the Pod
   Describe the pod to get more information about why it is in a Pending state:

```
kubectl describe pod <pod-name>
```

Look for events at the bottom of the output to see if there are any errors or warnings.

2. 1. Check Logs
      Check the logs of the pod to see if there are any errors:

￼kubectl logs <pod-name>

```

￼kubectl logs fastapi-7447b65c7-f8z9m
```

3. Verify Deployment
   Ensure that the fastapi deployment is correctly applied and running:

```

kubectl get deployments
kubectl describe deployment fastapi
```

4. Check Node Status
   Ensure that your nodes have enough resources to schedule the pod:

```
kubectl get nodes
```

5. Verify Services
   Ensure that the service is correctly configured and the pod is correctly labeled to match the service selector:

```

kubectl get services
kubectl describe service <service-name>
```

6. Check for Resource Requests and Limits
   Ensure that your pod's resource requests and limits are reasonable and that your cluster has enough resources to accommodate them. Here is an example of how to set resource requests and limits in your deployment:

   example is to update kubernetes/fastapi-deployment.yaml

from

```
containers:
    - name: fastapi
        image: peneh/fastapi4k8:latest
```

to

```
containers:
    - name: fastapi
        image: peneh/fastapi4k8:latest
        resources:
        requests:
            memory: "64Mi"
            cpu: "250m"
        limits:
            memory: "128Mi"
            cpu: "500m"
```

7. Check PersistentVolumeClaims (if applicable)
   If your pod is using PersistentVolumeClaims, ensure that the claims are bound and that the PersistentVolumes are available:

```

kubectl get pvc
kubectl get pv
```

8. Check for Image Pull Issues
   Ensure that the image specified in your deployment is accessible and can be pulled by the Kubernetes nodes. If you are using a private registry, make sure you have created the necessary image pull secrets.

9. Check Events
   Check for any events that might give more context about why the pod is pending:

```
kubectl get events
```

10. Apply Configurations Again
    If you have made any changes to the configurations, apply them again:

```

kubectl apply -f kubernetes/postgres-secret.yaml
kubectl apply -f kubernetes/postgres-config.yaml
kubectl apply -f kubernetes/postgres-deployment.yaml
kubectl apply -f kubernetes/postgres-service.yaml
kubectl apply -f kubernetes/fastapi-deployment.yaml
kubectl apply -f kubernetes/fastapi-service.yaml
kubectl apply -f kubernetes/fastapi-ingress.yaml

```

## mög not found

1. http://localhost:8080

kubectl port-forward service/fastapi 8080:80
Forwarding from 127.0.0.1:8080 -> 8000
Forwarding from [::1]:8080 -> 8000
Handling connection for 8080
Handling connection for 8080
E1211 14:20:14.624224 3483462 portforward.go:413] "Unhandled Error" err="an error occurred forwarding 8080 -> 8000: error forwarding port 8000 to pod 915bb370d91f40a28b8d3049f3687982b870ee580c3c9b08f6c294c312d23c5d, uid : failed to execute portforward in network namespace \"/var/run/netns/cni-a10b5c76-519a-07a8-f1ec-8fe1278ad318\": failed to connect to localhost:8000 inside namespace \"915bb370d91f40a28b8d3049f3687982b870ee580c3c9b08f6c294c312d23c5d\", IPv4: dial tcp4 127.0.0.1:8000: connect: connection refused IPv6 dial tcp6 [::1]:8000: connect: connection refused "
E1211 14:20:14.624227 3483462 portforward.go:413] "Unhandled Error" err="an error occurred forwarding 8080 -> 8000: error forwarding port 8000 to pod 915bb370d91f40a28b8d3049f3687982b870ee580c3c9b08f6c294c312d23c5d, uid : failed to execute portforward in network namespace \"/var/run/netns/cni-a10b5c76-519a-07a8-f1ec-8fe1278ad318\": failed to connect to localhost:8000 inside namespace \"915bb370d91f40a28b8d3049f3687982b870ee580c3c9b08f6c294c312d23c5d\", IPv4: dial tcp4 127.0.0.1:8000: connect: connection refused IPv6 dial tcp6 [::1]:8000: connect: connection refused "
error: lost connection to pod

1. 1. kubectl get pods
      NAME READY STATUS RESTARTS AGE
      fastapi-84cfcb4f6-j5n55 0/1 CrashLoopBackOff 6 (3m3s ago) 9m2s
      postgres-5865844c6d-m5nd5 1/1 Running 0 9m13s

### Direkt från Chat

Om du vill sätta upp FastAPI och PostgreSQL-containrar utan att använda Docker Compose, kan du göra det med individuella docker run-kommandon. Här är en steg-för-steg-guide:

1. Skapa FastAPI-projektet
   Skapa en mappstruktur:

mkdir fastapi-postgres
cd fastapi-postgres
mkdir app
Skapa filen app/main.py:

python
from fastapi import FastAPI
import psycopg2

app = FastAPI()

@app.get("/")
def read_root():
return {"message": "Welcome to FastAPI with PostgreSQL"}

@app.get("/db-test")
def test_db():
try:
conn = psycopg2.connect(
dbname="mydatabase",
user="postgres",
password="password",
host="localhost",
port="5432",
)
cur = conn.cursor()
cur.execute("SELECT 1;")
result = cur.fetchone()
cur.close()
conn.close()
return {"db_test": result}
except Exception as e:
return {"error": str(e)}

2. Skapa en Dockerfile för FastAPI
   Skapa en fil Dockerfile i huvudmappen:

dockerfile

# Dockerfile

FROM python:3.11-slim

WORKDIR /app
COPY ./app /app

RUN pip install --no-cache-dir fastapi uvicorn psycopg2-binary

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 3. Bygg Docker-bilden för FastAPI
Bygg bilden med följande kommando:

docker build -t fastapi-app .

4. Starta PostgreSQL-container
   Starta en PostgreSQL-container:

docker run --name postgres-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=mydatabase -p 5432:5432 -d postgres:15

5. Starta FastAPI-container
   Starta FastAPI-container och koppla den till PostgreSQL:

docker run --name fastapi-app --link postgres-db:db -e DATABASE_URL=postgresql://postgres:password@db:5432/mydatabase -p 8000:8000 fastapi-app

6. Testa applikationen
   Gå till http://localhost:8000 för att se FastAPI.
   Testa /db-test för att säkerställa att FastAPI kan ansluta till PostgreSQL.
   Förklaringar
   PostgreSQL-container

--name postgres-db: Namnger containern.
-e: Ställer in miljövariabler för användare, lösenord och databas.
-p 5432:5432: Exponerar port 5432.
FastAPI-container

--name fastapi-app: Namnger containern.
--link postgres-db:db: Kopplar FastAPI-container till PostgreSQL-container via aliaset db.
-e DATABASE_URL=...: Miljövariabel som används av FastAPI för att ansluta till databasen.

### test run

Att skapa en FastAPI-app som skriver till en PostgreSQL-databas i ett Kubernetes-kluster med k3s (en lightweight Kubernetes-distribution) kräver flera steg. Här är en steg-för-steg-guide:

1. Förbered din FastAPI-app
   Installera beroenden: Skapa en Python-miljö och installera nödvändiga bibliotek:

bash
￼Copy code
pip install fastapi uvicorn psycopg2-binary sqlalchemy
Exempel på FastAPI-app med PostgreSQL och SQLAlchemy:

python
￼Copy code
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@postgres-service.default.svc.cluster.local/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definiera en tabell

class Item(Base):
**tablename** = "items"
id = Column(Integer, primary_key=True, index=True)
name = Column(String, index=True)

# Initiera databasen

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/items/")
def create_item(name: str):
db = SessionLocal()
try:
new_item = Item(name=name)
db.add(new_item)
db.commit()
db.refresh(new_item)
return new_item
except Exception as e:
db.rollback()
raise HTTPException(status_code=500, detail=str(e))
finally:
db.close() 2. Skapa en PostgreSQL-databas i klustret
Använd en Kubernetes StatefulSet eller Helm Chart för PostgreSQL:

Med Helm:

bash
￼Copy code
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install postgres bitnami/postgresql \
 --set auth.username=user \
 --set auth.password=password \
 --set auth.database=dbname
Detta skapar en PostgreSQL-instans som är åtkomlig via postgres-service.default.svc.cluster.local inom klustret.

3. Dockerisera FastAPI-appen
   Skapa en Dockerfile för din app:

dockerfile
￼Copy code
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
Bygg och tagga bilden:

bash
￼Copy code
docker build -t fastapi-app:latest . 4. Skapa Kubernetes-manifest för FastAPI-appen
Deployment och Service för FastAPI:

yaml
￼Copy code
apiVersion: apps/v1
kind: Deployment
metadata:
name: fastapi-app
spec:
replicas: 2
selector:
matchLabels:
app: fastapi-app
template:
metadata:
labels:
app: fastapi-app
spec:
containers: - name: fastapi
image: fastapi-app:latest
ports: - containerPort: 8000
env: - name: DATABASE_URL
value: "postgresql://user:password@postgres-service.default.svc.cluster.local/dbname"

---

apiVersion: v1
kind: Service
metadata:
name: fastapi-service
spec:
selector:
app: fastapi-app
ports:

- protocol: TCP
  port: 80
  targetPort: 8000
  type: ClusterIP
  Spara ovanstående i en fil, t.ex. fastapi.yaml, och applicera det:

bash
￼Copy code
kubectl apply -f fastapi.yaml 5. Testa och verifiera
Exponera appen lokalt:

bash
￼Copy code
kubectl port-forward service/fastapi-service 8080:80
Skicka en POST-förfrågan till API:t:

bash
￼Copy code
curl -X POST "http://localhost:8080/items/" -H "Content-Type: application/json" -d '{"name": "Test Item"}' 6. Skala och hantera appen
Använd Kubernetes kommandon för att skala eller övervaka din FastAPI-app:

bash
￼Copy code
kubectl scale deployment fastapi-app --replicas=3
kubectl get pods
kubectl logs deployment/fastapi-app 7. Tips för produktion
Databasanslutning: Använd en Connection Pool Manager som asyncpg med Databases-biblioteket för bättre prestanda.
TLS: Använd en Ingress Controller som Traefik eller NGINX för att hantera HTTPS.
Secrets: Använd Kubernetes Secrets för databaslösenord och annan känslig information.
Behöver du fler detaljer?

￼
￼
￼
￼
￼
￼
You said:
Lägg till en funktion i main som lägger in user mail och id i databasen och sen läser innehållet
ChatGPT said:
ChatGPT
Här är en uppdaterad version av din FastAPI-app som inkluderar en funktion för att lägga till en användares e-postadress och ID i databasen och sedan läsa innehållet:

Uppdaterad kod för FastAPI-app
python
￼Copy code
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql://user:password@postgres-service.default.svc.cluster.local/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definiera tabeller

class User(Base):
**tablename** = "users"
id = Column(Integer, primary_key=True, index=True)
email = Column(String, unique=True, index=True)

# Initiera databasen

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency för att få en databas-session

def get_db():
db = SessionLocal()
try:
yield db
finally:
db.close()

# Lägg till en ny användare

@app.post("/users/")
def create_user(id: int, email: str, db: Session = Depends(get_db)):
try:
new_user = User(id=id, email=email)
db.add(new_user)
db.commit()
db.refresh(new_user)
return {"message": "User added successfully", "user": new_user}
except Exception as e:
db.rollback()
raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

# Läs alla användare från databasen

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
try:
users = db.query(User).all()
return {"users": users}
except Exception as e:
raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
Funktioner förklarade
/users/ (POST):

Tar emot id och email som indata.
Lägger till en ny användare i databasen.
Returnerar ett meddelande och information om användaren.
/users/ (GET):

Hämtar alla användare från databasen.
Returnerar en lista över alla användare.
Testa API:t
Lägg till en användare
Skicka en POST-förfrågan:

bash
￼Copy code
curl -X POST "http://localhost:8080/users/" \
-H "Content-Type: application/json" \
-d '{"id": 1, "email": "example@test.com"}'
Hämta alla användare
Skicka en GET-förfrågan:

bash
￼Copy code
curl -X GET "http://localhost:8080/users/" -H "Content-Type: application/json"
Uppdatera databasen i Kubernetes
Om tabellen users inte existerar i databasen än:

Radera eventuell tidigare FastAPI-pod:

bash
￼Copy code
kubectl delete pod <fastapi-pod-namn>
Starta om appen för att säkerställa att Base.metadata.create_all(bind=engine) skapar de nya tabellerna.

Nu kan din FastAPI-app hantera användardata! Vill du lägga till fler funktioner, till exempel uppdatering eller borttagning av användare?

￼
￼
￼
￼
￼
You said:
Kan man få DATABASEN_URL som variabler till yaml filen
ChatGPT said:
ChatGPT
Ja, du kan använda Kubernetes ConfigMaps och Secrets för att hantera variabler som DATABASE_URL i din YAML-fil. Det är en bra praxis att hålla känslig information, som databaslösenord, i Secrets, medan mindre känsliga variabler kan lagras i ConfigMaps.

1. Skapa en Secret för känslig information
   Skapa en Kubernetes Secret för att lagra användarnamn, lösenord och databasnamn.

Secret-manifest (secret.yaml):

yaml
￼Copy code
apiVersion: v1
kind: Secret
metadata:
name: postgres-secret
type: Opaque
data:
username: dXNlcg== # Bas64-kodad "user"
password: cGFzc3dvcmQ= # Bas64-kodad "password"
database: ZGJuYW1l # Bas64-kodad "dbname"
Du kan använda echo -n 'värde' | base64 för att skapa de Base64-kodade värdena.

Applicera Secret:

bash
￼Copy code
kubectl apply -f secret.yaml 2. Skapa en ConfigMap för mindre känslig information
Skapa en ConfigMap för databasens värdnamn och port.

ConfigMap-manifest (configmap.yaml):

yaml
￼Copy code
apiVersion: v1
kind: ConfigMap
metadata:
name: postgres-config
data:
host: "postgres-service.default.svc.cluster.local"
port: "5432"
Applicera ConfigMap:

bash
￼Copy code
kubectl apply -f configmap.yaml 3. Använd Secret och ConfigMap i din Deployment
Uppdatera din Deployment-manifestfil för att injicera miljövariabler i containern.

Uppdaterad Deployment (fastapi.yaml):

yaml
￼Copy code
apiVersion: apps/v1
kind: Deployment
metadata:
name: fastapi-app
spec:
replicas: 2
selector:
matchLabels:
app: fastapi-app
template:
metadata:
labels:
app: fastapi-app
spec:
containers: - name: fastapi
image: fastapi-app:latest
ports: - containerPort: 8000
env: - name: POSTGRES_USER
valueFrom:
secretKeyRef:
name: postgres-secret
key: username - name: POSTGRES_PASSWORD
valueFrom:
secretKeyRef:
name: postgres-secret
key: password - name: POSTGRES_DB
valueFrom:
secretKeyRef:
name: postgres-secret
key: database - name: POSTGRES_HOST
valueFrom:
configMapKeyRef:
name: postgres-config
key: host - name: POSTGRES_PORT
valueFrom:
configMapKeyRef:
name: postgres-config
key: port - name: DATABASE_URL
value: "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}" 4. Testa och verifiera
Applicera Deployment:

bash
￼Copy code
kubectl apply -f fastapi.yaml
Kontrollera miljövariablerna i podden:

bash
￼Copy code
kubectl exec -it <pod-namn> -- env
Du bör se DATABASE_URL korrekt konfigurerad.

Fördelar med denna metod
Säkerhet: Känslig information hanteras med Secrets.
Flexibilitet: Du kan ändra variabler utan att behöva uppdatera din applikation.
Skalbarhet: ConfigMaps och Secrets kan återanvändas av flera applikationer.
Vill du lägga till något mer, till exempel hur du roterar Secrets?
