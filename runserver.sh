#!/bin/sh
python3 manage.py migrate
python3 manage.py loaddata init_data.json
python3 manage.py loaddata auth.json
python3 manage.py runserver 0.0.0.0:8000
