# Blogicum

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)

Project made while learning Django on Yandex.Practicum.

Represents simple social network (like LJ) with posts, comments etc.

## Installation
Clone form GitHub:
```sh
git clone https://github.com/MuKeLaNGlo/django_sprint4.git
```
Install python virtual environment and requirements:
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Apply migrations:
```sh
python manage.py migrate
```
Create superuser if required:
```sh
python3 manage.py runserver
```

Premade fixtures can be applied with:
```sh
python manage.py loaddata ../dj.json
```
## Running project locally
Project can be started via:
```sh
python manage.py runserver
```
It will run project on local server on 8000 port: http://localhost:8000/
___
### Credits
Developed by Nikolai Petrishchev, 2023.