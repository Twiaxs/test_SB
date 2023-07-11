#!/bin/sh

sleep 2
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input 

exec "$@"
