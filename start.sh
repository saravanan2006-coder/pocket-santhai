#!/bin/bash
# Apply database migrations
python manage.py migrate --noinput

# Auto-create superuser 'boss' with password 'admin123' if no superuser exists, and ensure they have a role
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(is_superuser=True).exists() or User.objects.create_superuser('boss', 'admin@example.com', 'admin123', role='retailer', email_verified=True); User.objects.filter(is_superuser=True).update(role='retailer', email_verified=True)"

# Start the Celery worker in the background with minimum memory footprint
celery -A marketplace worker -l INFO --concurrency 1 &

# Start the Django web server with minimum memory footprint
gunicorn marketplace.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 2
