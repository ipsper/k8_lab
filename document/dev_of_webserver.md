# Här är ett exempel på en FastAPI-server som använder en PostgreSQL-databas och är redo att köras i Kubernetes. Exemplet inkluderar:

## setup in vent

```
cd $HOME/repo/k8_lab
python3 -m venv k8_lab_venv
source k8_lab_venv/bin/activate
python -m pip install -r app/requirements.txt
```

## Load the environment variables in your shell

```

export POSTGRES_DB=mydatabase
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=your_password
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
```

## start webserver

```
k8_lab_venv/bin/uvicorn app.main:app --reload
k8_lab_venv/bin/uvicorn app.main:app --host 81.170.169.84 --port 8080
k8_lab_venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

```

## To exit

```
deactivate
```

## To delete vent

```
rm -rf $HOME/repo/k8_lab/k8_lab_venv
```

# sparka igång postgres

1. Ensure PostgreSQL Server is Running
   Make sure the PostgreSQL server is running. You can start the PostgreSQL server using the following command:

Check the status of the PostgreSQL server:
￼`
sudo systemctl status postgresql
￼`
om Unit postgresql.service could not be found.

￼```
sudo systemctl start postgresql

```

￼
sudo systemctl status postgresql 2. Verify PostgreSQL Configuration
Ensure that PostgreSQL is configured to accept connections on localhost and port 5432. You can check the PostgreSQL configuration file (postgresql.conf) and the pg_hba.conf file.

Edit the postgresql.conf file to ensure it is listening on the correct address:

￼
sudo nano /etc/postgresql/12/main/postgresql.conf
Ensure the following line is present and uncommented:

￼
listen_addresses = 'localhost'
Edit the pg_hba.conf file to ensure it allows connections from localhost:

￼
sudo nano /etc/postgresql/12/main/pg_hba.conf
Ensure the following line is present:

￼
host all all 127.0.0.1/32 md5
After making changes to the configuration files, restart the PostgreSQL server:

￼
sudo systemctl restart postgresql

3. Verify Environment Variables
Ensure that the environment variables for the database configuration are correctly set. You can set them in your shell or in a .env file.

## Other documentation
```
