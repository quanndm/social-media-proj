# SOCIAL MEDIA PROJECT
## What's inside?
This is project social media

#### Note
- The server api is located in ```/server``` folder and is built with Django
- The frontend is located in ```/frontend``` folder and is built with Nextjs
##### Important: To avoid issue, always open the root folder in VS Code.      


## Backend setup
### Create new virtual environment
```
python -m venv env
```
### Use env
```
.\env\Scripts\activate
```
### install package 
```
pip install -r ./requirements.txt
```
### delete db.sqlite3 if exists
### Create the initial migrations and generate the database schema:
```
python manage.py makemigrations
python manage.py migrate
```
### In django-proj-api\myAuth\serializers.py, line 37 - 38, comment them and create a super account, after create comment again
### start project 
```
python.exe .\manage.py runserver
```

## Frontend Setup
### Install node module
```
npm install
```
### DEV Server
```
npm run dev
```