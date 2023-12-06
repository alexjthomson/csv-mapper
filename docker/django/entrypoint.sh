#!/bin/bash

# Change the CWD to the code directory:
cd /code

# Apply database migratons:
python3 manage.py makemigrations
python3 manage.py migrate

# Start the Django server
python3 manage.py runserver 0.0.0.0:8000