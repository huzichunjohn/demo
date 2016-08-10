## Requirements
* Python 2.7
* Django 1.8

## Quick start
1. ```pip install -r requirements.txt```
2. ```python manage.py runserver 0.0.0.0:8000```

## Gunicorn
```gunicorn -w 4 wsgi:application -b 0.0.0.0:8000 --name demo --worker-class=gevent```
