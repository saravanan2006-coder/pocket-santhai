web: gunicorn marketplace.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A marketplace worker -l INFO
