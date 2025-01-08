# install postgresql

1. ubuntu

- [linux ubuntu](https://ubuntu.com/server/docs/install-and-configure-postgresql)

```
sudo apt install postgresql
```

sudo systemctl status postgresql

2. Verify PostgreSQL Configuration
   Ensure that PostgreSQL is configured to accept connections on localhost and port 5432. You can check the PostgreSQL configuration file (postgresql.conf) and the pg_hba.conf file.

Edit the postgresql.conf file to ensure it is listening on the correct address:

get version

```
ls /etc/postgresql/ | head -1
```

sudo vi /etc/postgresql/<version>/main/postgresql.conf
sudo vi /etc/postgresql/16/main/postgresql.conf

Ensure the following line is present and uncommented:

￼
listen_addresses = 'localhost'
Edit the pg_hba.conf file to ensure it allows connections from localhost:

￼
sudo vi /etc/postgresql/<version>/main/pg_hba.conf
sudo vi /etc/postgresql/16/main/pg_hba.conf
Ensure the following line is present:

￼
host all all 127.0.0.1/32 md5
After making changes to the configuration files, restart the PostgreSQL server:

￼
sudo systemctl restart postgresql

3. Verify Environment Variables
   Ensure that the environment variables for the database configuration are correctly set. You can set them in your shell or in a .env file.

# install postgresql-client

```
sudo apt install postgresql-client
```

```
psql --host localhost --username postgres --password --dbname mydatabase

```

## funkar inte

(k8_lab_venv) per@per-PN52:~/repo/k8_lab$ psql --host localhost --username postgres --password --dbname mydatabase
Password:
psql: error: connection to server at "localhost" (127.0.0.1), port 5432 failed: FATAL: password authentication failed for user "postgres"
connection to server at "localhost" (127.0.0.1), port 5432 failed: FATAL: password authentication failed for user "postgres"
