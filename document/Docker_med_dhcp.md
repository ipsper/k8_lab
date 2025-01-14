## Nej, en Docker-container kan inte direkt tilldelas en IP-adress från en DHCP-server eftersom Docker skapar sina egna nätverksgränssnitt och hanterar nätverk internt. Dockers standardinställning använder ett internt nätverk där containrar får IP-adresser tilldelade från Docker själv.

Alternativ för att hantera nätverksinställningar
Om du vill att en Docker-container ska få en specifik IP-adress eller fungera som en "vanlig" maskin på ditt lokala nätverk kan du använda följande metoder:

1. Bridge Network med Fastställd IP
   Du kan skapa ett anpassat Docker-nätverk och tilldela en statisk IP-adress till containern:

Steg:
Skapa ett anpassat Docker-nätverk:

docker network create \
 --subnet=192.168.1.0/24 \
 my_custom_network
Starta containern med en specifik IP-adress:

docker run --net my_custom_network --name your_name --ip 192.168.1.100 -p 8080:8080 fastapi-app
Begränsning:
Containern är fortfarande inte på samma nätverk som din DHCP-server, men den får en fast IP inom Dockers nätverk. 2. Host Network
Använd Docker's host network för att köra containern på värdmaskinens nätverk. Då delar containern nätverksgränssnitt med värden.

Steg:
Starta containern med flaggan --network=host:

docker run --network=host fastapi-app
Containern kommer nu att använda värdmaskinens IP-adress.

Begränsning:
Endast tillgängligt på Linux.
Alla portar i containern är direkt exponerade på värdmaskinens nätverk. 3. Macvlan Network
Docker's macvlan-drivrutin kan användas för att skapa ett nätverk där containrarna får en egen virtuell MAC-adress och kan tilldelas IP-adresser från en DHCP-server.

Steg:
Skapa ett macvlan-nätverk:

docker network create \
 --driver macvlan \
 --subnet=192.168.1.0/24 \
 --gateway=192.168.1.1 \
 --ip-range=192.168.1.100/28 \
 -o parent=eth0 \
 fastapi_net
Starta containern på macvlan-nätverket:

docker run --net my_macvlan_network --ip 192.168.1.101 fastapi-app
Fördel:
Containern fungerar som en separat maskin på det lokala nätverket.
Den kan kommunicera direkt med andra enheter på nätverket.
Begränsning:
Konfiguration av macvlan kan vara komplicerad.
Värdmaskinen kan inte kommunicera direkt med containern utan ytterligare nätverkskonfiguration.
Rekommendation
Om du vill att containern ska uppträda som en "vanlig maskin" på ditt lokala nätverk, är macvlan det bästa alternativet. Det låter dig tilldela en IP från ditt befintliga nätverk, antingen manuellt eller via DHCP.

### Ja, det går att köra flera FastAPI-app-containrar med olika IP-adresser i Docker. Här är några metoder för att uppnå detta:

1. Använda Ett Anpassat Docker Bridge Network
   Du kan skapa ett anpassat Docker-nätverk och tilldela specifika IP-adresser till varje container.

Steg:
Skapa ett anpassat nätverk:

docker network create --subnet=192.168.33.0/24 fastapi_network

docker network create --driver macvlan --subnet=192.168.33.0/24 --gateway=192.168.33.1 --ip-range=192.168.33.96/28 -o parent=enp2s0 fastapi_macvlan_network

Kör containrar med specifika IP-adresser:

docker run -it --net fastapi_macvlan_network --name fastapi-app-101 --ip 192.168.33.101 -p 8001:8000 peneh/fastapi4k8
docker run -it --net fastapi_network --name fastapi-app-101 --ip 192.168.33.101 -p 8001:8000 fastapi-app

docker run -it --net fastapi_network --name fastapi-app-102 --ip 192.168.33.102 -p 8002:8000 fastapi-app

Åtkomst till containrarna:

http://192.168.33.101:8001
http://192.168.33.102:8002
Begränsningar:
Nätverket måste administreras manuellt, inklusive att säkerställa att IP-adresser inte kolliderar.

2. Använda Docker Macvlan
   Med macvlan-drivrutinen kan varje container få en egen IP-adress från det lokala nätverket.

## hitta länk

mac

```

ifconfig | grep -B 6 'status: active'
```

linux

```

ip link show
```

Steg:
Skapa ett macvlan-nätverk:

docker network create \
 --driver macvlan \
 --subnet=192.168.1.0/24 \
 --gateway=192.168.1.1 \
 --ip-range=192.168.1.100/28 \
 -o parent=<link> \
 fastapi_net

- mac

docker network create \
 --driver macvlan \
 --subnet=192.168.1.0/24 \
 --gateway=192.168.1.1 \
 --ip-range=192.168.1.96/28 \
 -o parent=awdl0 \
 fastapi_net

- linux ubuntu

docker network create \
 --driver macvlan \
 --subnet=192.168.1.0/24 \
 --gateway=192.168.1.1 \
 --ip-range=192.168.1.96/28 \
 -o parent=enp2s0 \
 fastapi_net

Kör flera containrar:

- linux ubuntu

docker run -d --name postgres-db --net fastapi_net --ip 192.168.1.120 \
 -e POSTGRES_DB=dbname \
 -e POSTGRES_USER=user \
 -e POSTGRES_PASSWORD=your_password \
 -p 5432:5432 \
 postgres:13

docker run -d --name fastapi-app-101 --net fastapi_net --ip 192.168.1.101 \
 -e POSTGRES_DB=dbname \
 -e POSTGRES_USER=user \
 -e POSTGRES_PASSWORD=your_password \
 -e POSTGRES_HOST=192.168.1.120 \
 -e POSTGRES_PORT=5432 \
 -e UVICORN_HOST=0.0.0.0 \
 -e UVICORN_PORT=8000 \
 peneh/fastapi4k8:latest

- mac

docker run -d --name fastapi-app-101 --net fastapi_net --ip 192.168.1.101 \
 -e POSTGRES_DB=dbname \
 -e POSTGRES_USER=user \
 -e POSTGRES_PASSWORD=your_password \
 -e POSTGRES_HOST=192.168.1.120 \
 -e POSTGRES_PORT=5432 \
 -e UVICORN_HOST=0.0.0.0 \
 -e UVICORN_PORT=8000 \
 peneh/fastapi4k8onmacos:latest

docker run -d --name fastapi-app-102 --net fastapi_net --ip 192.168.1.102 \
 -e POSTGRES_DB=dbname \
 -e POSTGRES_USER=user \
 -e POSTGRES_PASSWORD=your_password \
 -e POSTGRES_HOST=192.168.1.120 \
 -e POSTGRES_PORT=5432 \
 -e UVICORN_HOST=0.0.0.0 \
 -e UVICORN_PORT=8000 \
 peneh/fastapi4k8:latest

docker run -d --name fastapi-app -p 8000:8000 \
 -e POSTGRES_DB=dbname \
 -e POSTGRES_USER=user \
 -e POSTGRES_PASSWORD=your_password \
 -e POSTGRES_HOST=localhost \
 -e POSTGRES_PORT=5432 \
 -e UVICORN_HOST=0.0.0.0 \
 -e UVICORN_PORT=8000 \
 fastapi-app

Åtkomst till containrarna:

http://192.168.1.101:8000
http://192.168.1.102:8000
Fördelar:
Varje container fungerar som en separat enhet i ditt lokala nätverk.
Kan få IP-adresser från DHCP-servern.
Begränsningar:
Kräver viss konfiguration på nätverksnivå.
Containrar kan inte direkt kommunicera med värdmaskinen utan extra konfiguration.

3. Använda Kubernetes
   Om du vill ha fler containrar som hanteras dynamiskt med olika IP-adresser är Kubernetes ett bra alternativ. Varje pod i Kubernetes får en unik IP-adress.

Exempel:
Skapa en Deployment för flera FastAPI-appar:

yaml
apiVersion: apps/v1
kind: Deployment
metadata:
name: fastapi-apps
spec:
replicas: 3
selector:
matchLabels:
app: fastapi
template:
metadata:
labels:
app: fastapi
spec:
containers: - name: fastapi
image: fastapi-app:latest
ports: - containerPort: 8000
När du använder Kubernetes kan varje pod ha en unik intern IP-adress.

Rekommendation
För lokala utvecklingsändamål: Anpassat Bridge Network är enkelt att sätta upp.
För avancerad nätverkskonfiguration: Macvlan låter containrar agera som "fullvärdiga" nätverksdeltagare.
För skalbarhet och orkestrering: Kubernetes är det bästa alternativet.
