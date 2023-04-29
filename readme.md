# Requirements

## Database requirements

install local postgres instance

please use POSTGRES_PASSWORD value from
[config.ini](config.ini)

```
docker pull postgres
docker run -d --name full-stack-challenge-db -e POSTGRES_PASSWORD=<password> -p 5432:5432 postgres
```
start postgres instance

```
docker start full-stack-challenge-db
```

once connected to instance execute create database script in editor
[create_database.sql](resources%2Fdatabase%2Fcreate_database.sql)

connect to "Assets" database using editor.
execute scripts from 
[create_schema_tables_initial_data.sql](resources%2Fdatabase%2Fcreate_schema_tables_initial_data.sql)

## Project package requirements
to install requirements need for project run  
```
pip install -r requirements.txt
```

## start server 
to start the application use

```
flask run --port 12000
```

it will start the project at port 12000