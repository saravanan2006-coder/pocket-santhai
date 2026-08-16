#!/bin/bash
# Apply database migrations
python manage.py migrate --noinput

# Auto-create superuser 'boss' with password 'admin123' if no superuser exists
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(is_superuser=True).exists() or User.objects.create_superuser('boss', 'admin@example.com', 'admin123')"

# Start the Celery worker in the background
celery -A marketplace worker -l INFO &

# Start the Django web server
gunicorn marketplace.wsgi:application --bind 0.0.0.0:$PORT
