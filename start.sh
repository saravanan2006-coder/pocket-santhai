#!/bin/bash
# Apply database migrations
python manage.py migrate --noinput

# Auto-create superuser if no superuser exists (configurable via env vars, fallback for backwards compatibility)
python manage.py shell -c "import os; from django.contrib.auth import get_user_model; User = get_user_model(); u = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'boss'); e = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com'); p = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123'); User.objects.filter(is_superuser=True).exists() or User.objects.create_superuser(u, e, p, role='retailer', email_verified=True); User.objects.filter(is_superuser=True, role='').update(role='retailer', email_verified=True)"

# Start the Celery worker in the background with minimum memory footprint
celery -A marketplace worker -l INFO --concurrency 1 &

# Start the Django web server with minimum memory footprint
gunicorn marketplace.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 2
