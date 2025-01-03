4. Dra ner din image from DockerHub

docker pull <username>/<repository-name>:<tag>

- Exempel:

```

docker pull peneh/fastapi4k8:latest

docker pull postgres

```

### mac

```
docker pull peneh/fastapi4k8onmacos:latest
docker pull postgres

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

## start postgres

docker run --name postgres-container -e POSTGRES_PASSWORD=mysecretpassword -d postgres

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
