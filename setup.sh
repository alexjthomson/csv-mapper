#!/bin/bash

# This script will setup the Docker environment for the Django project.

# Data directory:
mkdir ./data
mkdir ./data/mysql

# Log directory:
mkdir ./log
mkdir ./log/django

# Source directory:
mkdir ./src

# Secrets directory:
mkdir ./.secrets

# Django secret key:
touch ./.secrets/django_secret_key
openssl rand -hex 64 > ./.secrets/django_secret_key

# MySQL root user:
touch ./.secrets/mysql_root_password
openssl rand -hex 64 > ./.secrets/mysql_root_password

# MySQL django user:
touch ./.secrets/mysql_django_password
openssl rand -hex 64 > ./.secrets/mysql_django_password

# Docker:
sudo docker-compose down --remove-orphans --rmi all --volumes
sudo docker-compose up --force-recreate --build -d && sudo docker-compose down
sudo docker image prune -f

# Python Requirements:
pip-compile --generate-hashes -o requirements.txt

sudo docker-compose up -d
