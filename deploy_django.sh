#!/usr/bin/env bash

source env/bin/activate &&
cd iscte50anos &&

export DJANGO_SECRET_KEY=$(openssl rand -hex 40) &&
export MYSQL_USER="iscteSpots" &&
export MYSQL_PASS="o iscte e uma ganda uni" &&
export MYSQL_HOST="localhost" &&
export MYSQL_PORT=3306

python manage.py makemigrations &&
python manage.py migrate &&

echo "from __scripts import run" | python manage.py shell &&

gunicorn --workers=9 iscte50anos.wsgi 