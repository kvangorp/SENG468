# SENG 468 Project

## Group Information

**Group Name**: Hermes (Group 5)  
**Language**: Python  
**Platforms and Tools**: MongoDB, Django, React

## Setting up dev environment:

Will need to have Docker and docker-compose installed.

- To start up the mongoDB database, go to the root directory of the project (where the docker-compose.yml file is located) and run:
```
docker-compose up
```

- To start up the django backend, go in to the TransactionServer directory and run:

```
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt

cd src
python manage.py migrate
python manage.py runserver
```

- If you go to http://localhost:8000/api/<stocks|quotes|triggers>, you can interact with the django rest api.

- You can check out the contents of the database by connecting to the mongodb container using the interactive docker terminal, and then opening up the mongo shell:
```
docker exec -it mongodb bash
mongo
```
- There's a list of mongo shell commands [here](https://docs.mongodb.com/manual/reference/mongo-shell/). For example, to see all collections you can run:
```
use ariesdb
show collections
```
