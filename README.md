# Astra Web App

The application parses a XML file with inventory supplies and provides following pieces of information:

- Task 1: Count of unique items (calculated as a number of unique product codes).
- Task 2: List of items with code and name.
- Task 3: List of replaceable parts for items that have at least one of them.

## How to run the application

Requirements: Docker and Docker Compose installed on the system. Before running the apps, files `.env` and `.env.db`
need to be created. The database name, username and password must match in both files. The debug should be set to `False`
in can of running the app on publicly accesible server.

Example `.env`:

```
DJANGO_ALLOWED_HOSTS=
DJANGO_SETTINGS_MODULE=AstraWebApp.settings
SECRET_KEY=f
SQL_DATABASE=
SQL_ENGINE=django.db.backends.postgresql
SQL_HOST=db
SQL_PASSWORD=
SQL_PORT=5432
SQL_USER=
FORM_PASSWORD=
DEBUG=
```

Example `.env.db`

```
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
```

To start the up, run following commands:

```
docker-compose build
docker-compose up
docker exec -it astrawebapp_web_1 python3 manage.py migrate
```
