#!/bin/sh
python3 manage.py collectstatic --noinput
python3 manage.py migrate
#python3 manage.py loaddata init_data.json
#python3 manage.py loaddata auth.json
exec gunicorn -b :8000 --access-logfile - --error-logfile - pages_app.wsgi:application
