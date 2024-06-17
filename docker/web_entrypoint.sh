#!/bin/sh

echo "--> Waiting for db to be ready"
./wait-for-it.sh db:5432

# cd OrderService

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --clear --noinput
python manage.py collectstatic --noinput

# Start server
echo "--> Starting web process"
gunicorn config.wsgi:application -b 0.0.0.0:8002
