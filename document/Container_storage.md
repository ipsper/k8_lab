# container storage

## DockerHub är en populär plats för att lagra och hantera Docker-images. Det är en offentlig container registry som gör det enkelt att dela och distribuera images

## du kan använda GitHub som en alternativ plats för att lagra och hantera Docker-images genom att använda GitHub Container Registry (GHCR). GHCR är en container registry som är inbyggd i GitHub och fungerar på ett liknande sätt som DockerHub. Här är hur du kan använda det:

1. Skapa ett GitHub Personal Access Token
   Gå till Settings > Developer settings > Personal access tokens på GitHub.
   Generera ett token med tillstånd för write:packages och read:packages.
2. Logga in till GHCR från Docker CLI
   Kör följande kommando i terminalen och ange ditt GitHub-användarnamn och token:

echo <PAT> | docker login ghcr.io -u <username> --password-stdin

3. Bygga och tagga en image
   Bygg och tagga din Docker-image för GHCR:

docker build -t ghcr.io/<username>/<image-name>:<tag> .

4. Push din image till GHCR
   När bilden är byggd och taggad kan du pusha den till GitHub Container Registry:

docker push ghcr.io/<username>/<image-name>:<tag>

5. Dra ner en image från GHCR
   För att använda en bild från GHCR kan du dra ner den med:

docker pull ghcr.io/<username>/<image-name>:<tag>
Fördelar med att använda GitHub som DockerHub
Integration: Om du redan använder GitHub för källkodshantering är det smidigt att hålla allt på ett ställe.
Åtkomstkontroll: Du kan använda GitHub-repositoriets befintliga åtkomstregler för att styra vem som får tillgång till dina images.
Kostnad: GitHub erbjuder gratis lagring och överföring inom vissa gränser.
Nackdelar
DockerHub är fortfarande mer etablerat för containerdistribution och har fler användare.
Om du använder Docker-compose eller andra verktyg kan du behöva konfigurera lite extra för att använda GHCR.

# Skapa ett nytt repository

Efter inloggning, klicka på Repositories i menyn.
Klicka på Create Repository.
Fyll i följande detaljer:
Repository name: Ange ett namn för ditt repo (t.ex. my-docker-image).
Description (valfritt): Beskriv vad detta repository är för.
Visibility: Välj mellan:
Public: Alla kan se och dra ner din image.
Private: Endast du och de du delar det med har åtkomst.
Klicka på Create för att skapa ditt repository.

1. Logga in på DockerHub från Docker CLI
   Öppna terminalen och kör:

docker login
Ange ditt DockerHub-användarnamn och lösenord när du ombeds.

- Exempel:

```
docker login -u peneh
```

2. Bygga och tagga din Docker-image
   Skapa din Docker-image och tagga den så att den pekar på ditt DockerHub-repo:

```

docker build -t peneh/fastapi4k8:latest .
```

## för mac

```

docker build -t peneh/fastapi4k8onmacos:latest .
```

docker build -t <username>/<repository-name>:<tag> .

- Exempel:

```k8_lab_venv

docker build -t peneh/fastapi4k8:latest .
```

3. Push din image till DockerHub
   Pusha den taggade imagen till DockerHub:

docker push <username>/<repository-name>:<tag>

- Exempel:

```
docker push peneh/fastapi4k8:latest
```

### mac

```
docker push peneh/fastapi4k8onmacos:latest

```

4. Verifiera i DockerHub
   Gå tillbaka till DockerHub och öppna ditt repository.
   Du bör nu se din image och tagg där. 5. Dra ner din image
   För att använda imagen från DockerHub kan du köra:

docker pull <username>/<repository-name>:<tag>

- Exempel:

```

docker pull peneh/fastapi4k8:latest
```

### mac

```
docker pull peneh/fastapi4k8onmacos:latest

```

Tips
Automatiska byggen: Du kan länka ditt DockerHub-repo till GitHub eller Bitbucket för att automatiskt bygga och pusha images när du gör commits.
Hantera åtkomst: För privata repos kan du lägga till teammedlemmar eller specifika användare under inställningarna.

# To start your container from the FastAPI project, follow these steps:

1. Build the Docker Image
   Run the following command in the root of your project directory (where your Dockerfile is located):

bash

```
docker build -t fastapi-app .

```

This will create a Docker image named fastapi-app.

2. setup the network

```
docker network create fastapi-network

```

3. Run the Docker Container
   Start a container from the built image. You need to connect it to the PostgreSQL database.

a. If PostgreSQL is running locally:
Use the following command:

docker run -d --name fastapi-container \
 -e DATABASE_URL="postgresql://user:password@host:port/db" \
 -p 8000:8000 fastapi4k8:latest

Replace:

user with

```
echo -n "postgres" | base64
```

password with

```
echo -n "password" | base64
```

docker run -d --name fastapi-container \
 -e DATABASE_URL="postgresql://cG9zdGdyZXM=:cGFzc3dvcmQ=@localhost:8080/db" \
 -p 8000:8000 fastapi4k8:latest

### mac

```
docker run -d --name fastapi-container \
 -e DATABASE_URL="postgresql://cG9zdGdyZXM=:cGFzc3dvcmQ=@localhost:8080/db" \
 -p 8000:8000 fastapi4k8onmacos:latest

```

user: PostgreSQL username
password: PostgreSQL password
host: Host where the database is running (localhost or container name if using Docker Compose)
port: Database port (default is 5432)
db: Database name
This command:

Runs the container in detached mode (-d).
Sets the environment variable DATABASE_URL for database connectivity.
Maps port 8000 of the container to port 8000 of your machine.
b. If PostgreSQL is running in another Docker container:
Use Docker's internal networking by referring to the database container by its name (e.g., postgres):

docker network create fastapi-network

# Run PostgreSQL container

docker run -d --name postgres --network fastapi-network \
 -e POSTGRES_USER=user \
 -e POSTGRES_PASSWORD=password \
 -e POSTGRES_DB=db \
 postgres:15

# Run FastAPI container

docker run -d --name fastapi-container --network fastapi-network \
 -e DATABASE_URL="postgresql://user:password@postgres:5432/db" \
 -p 8000:8000 fastapi-app
This connects both containers via the fastapi-network Docker network.

3. Access Your Application
   After starting the container, your FastAPI app will be available at:

http://localhost:8000 4. Stopping the Container
To stop the container:

docker stop fastapi-container
To remove it:

docker rm fastapi-container
