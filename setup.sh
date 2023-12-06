#!/bin/bash

# This script will setup the Docker environment for the Django project.

# Data directory:
mkdir ./data
mkdir ./data/mysql

# Logs directory:
mkdir ./logs
mkdir ./logs/django

# Source directory:
mkdir ./src

# Secrets directory:
mkdir ./.secrets

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

#sudo docker compose run django django-admin startproject csv_mapper . && sudo docker-compose down
sudo docker-compose up -d
