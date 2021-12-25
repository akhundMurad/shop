#!/bin/bash

cd src
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

celery -A backend.celery worker -l info
celery -A backend.celery beat --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler
python manage.py setupperiodicttasks

exit 0