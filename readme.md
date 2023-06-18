# before installed create new virtual environment
python -m venv env
# install package 
pip install -r ./requirements.txt
# delete db.sqlite3
# Create the initial migrations and generate the database schema:
```
python manage.py makemigrations
python manage.py migrate
```
# start project 
python.exe .\manage.py runserver