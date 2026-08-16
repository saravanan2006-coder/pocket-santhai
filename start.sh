#!/bin/bash
# Apply database migrations
python manage.py migrate --noinput

# Start the Celery worker in the background
celery -A marketplace worker -l INFO &

# Start the Django web server
gunicorn marketplace.wsgi:application --bind 0.0.0.0:$PORT
