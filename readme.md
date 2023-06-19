# before installed create new virtual environment
```
python -m venv env
```
# use env created before
```
.\env\Scripts\activate
```
# install package 
```
pip install -r ./requirements.txt
```
# delete db.sqlite3 if exists
# Create the initial migrations and generate the database schema:
```
python manage.py makemigrations
python manage.py migrate
```
# In django-proj-api\myAuth\serializers.py, line 37 - 38, comment them and create a super account, after create comment again
# start project 
```
python.exe .\manage.py runserver
```