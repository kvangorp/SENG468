# SENG 468 Project

**Group Name**: Hermes (Group 5)  
**Language**: Python  
**Platforms and Tools**: Postgres, Django, React, Node

## Setting up dev environment:

Will need to have Docker and docker-compose installed.

- In root directory of project, stop any running containers by running:
```
docker container prune
```
- Start up db by running:
```
docker-compose run
```
- To start up django backend, go to TransactionServer folder and run:

```
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt

cd src
python manage.py migrate
python manage.py runserver
```

- If you go to http://localhost:8080, you can sign in with username: root, pwd: seng468 and interact with the "ariesdb" database. There are some other dbs in there that come with Adminer and can be ignored.

- If you go to http://localhost:8000/api/<stocks|quotes|triggers>, you can interact with the django rest api.