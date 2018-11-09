#!/usr/bin/env bash
python manage.py migrate
python manage.py makemigrations portal
python manage.py migrate portal