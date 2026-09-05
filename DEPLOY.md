# Pocketசந்தை (PocketSanthai) — Deployment Guide

This guide covers deploying Pocketசந்தை to production, with detailed instructions for **Render.com** and general containerized/VPS environments.

---

## 1. Quick Deploy on Render.com (Blueprint)

Pocketசந்தை includes a declarative `render.yaml` configuration for Render Blueprints.

### Services Defined:
1. **PostgreSQL Database (`wholesale-db`)**: Managed database with persistent storage.
2. **Redis Service (`pocket-santhai-redis`)**: Valkey/Redis instance for session caching, Celery task queuing, and brute-force rate limiting.
3. **Web Service (`pocket-santhai`)**: Runs Gunicorn and WhiteNoise static serving, plus background Celery worker via `start.sh`.

### Steps to Deploy:
1. Push your repository to GitHub or GitLab.
2. Log in to [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** → **Blueprint**.
4. Select your PocketSanthai repository.
5. Render will detect `render.yaml` and configure the database, Redis instance, and web service automatically.
6. Under **Environment Variables**, fill in any required non-synced keys (e.g. `ANYMAIL_SENDINBLUE_API_KEY`, `VERIFICATION_DOMAIN`).
7. Click **Apply**. Render will run the build command:
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput
   ```
   and launch using:
   ```bash
   bash start.sh
   ```

---

## 2. Environment Variables Reference

| Variable | Required | Default | Description |
| :--- | :---: | :--- | :--- |
| `DJANGO_SECRET_KEY` | **Yes** | Auto-generated in Render | Strong random secret key for cryptography |
| `DJANGO_DEBUG` | **Yes** | `False` | Must be `False` in production |
| `DJANGO_ALLOWED_HOSTS` | **Yes** | `localhost,127.0.0.1` | Comma-separated domains allowed (e.g. `pocketsanthai.com,*.onrender.com`) |
| `CSRF_TRUSTED_ORIGINS` | **Yes** | (empty) | Comma-separated URLs with scheme (e.g. `https://pocketsanthai.com`) |
| `DATABASE_ENGINE` | No | `django.db.backends.postgresql` | Database engine |
| `DATABASE_NAME` | **Yes** | `wholesale_db` | PostgreSQL database name |
| `DATABASE_USER` | **Yes** | `wholesale_user` | PostgreSQL database username |
| `DATABASE_PASSWORD` | **Yes** | (generated) | PostgreSQL database password |
| `DATABASE_HOST` | **Yes** | (internal host) | PostgreSQL host |
| `DATABASE_PORT` | No | `5432` | PostgreSQL port |
| `DATABASE_CONN_MAX_AGE` | No | `300` | Database persistent connection age in seconds |
| `REDIS_URL` | **Yes** | (from service) | Redis/Valkey connection string |
| `EMAIL_BACKEND_API` | No | `True` | Set `True` to use Brevo API via Anymail |
| `ANYMAIL_SENDINBLUE_API_KEY` | No | (empty) | Brevo/Sendinblue API Key (avoids SMTP block) |
| `DEFAULT_FROM_EMAIL` | No | `noreply@pocketsanthai.com` | From email address for verification emails |
| `VERIFICATION_DOMAIN` | No | `localhost:8000` | Production domain used in verification links |
| `DJANGO_SUPERUSER_USERNAME` | No | `boss` | Initial superuser username |
| `DJANGO_SUPERUSER_EMAIL` | No | `admin@example.com` | Initial superuser email |
| `DJANGO_SUPERUSER_PASSWORD` | No | `admin123` | Initial superuser password |
| `SENTRY_DSN` | No | (empty) | Optional Sentry project DSN for error monitoring |

---

## 3. Email Delivery Setup (Brevo / Anymail)

Cloud providers like Render block outbound SMTP ports (`25`, `465`, `587`) by default. Pocketசந்தை uses `django-anymail` to deliver emails over HTTP REST API to Brevo (Sendinblue).

1. Register at [Brevo (Sendinblue)](https://www.brevo.com/).
2. Generate an API Key under **Account → SMTP & API → API Keys**.
3. In Render Environment Variables:
   - `EMAIL_BACKEND_API=True`
   - `ANYMAIL_SENDINBLUE_API_KEY=<your_brevo_api_key>`
   - `DEFAULT_FROM_EMAIL=<verified_sender_email_in_brevo>`
   - `VERIFICATION_DOMAIN=your-app-name.onrender.com`

---

## 4. Background Workers & Concurrency

### Free Tier Single-Container Setup:
On Render's Free tier, running separate background worker services can exceed free limits. `start.sh` executes the Celery worker in the background alongside Gunicorn:
```bash
# In start.sh:
celery -A marketplace worker -l INFO --concurrency 1 &
gunicorn marketplace.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 2
```

### Dedicated Worker Scaling (Paid / Production VPS):
For high-traffic deployments, split web and worker processes using the provided `Procfile`:
- **Web Service**:
  ```bash
  gunicorn marketplace.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --threads 2
  ```
- **Worker Service**:
  ```bash
  celery -A marketplace worker -l INFO --concurrency 2
  ```

---

## 5. Security & Verification Checklist

- [x] Ensure `DJANGO_DEBUG=False` in production.
- [x] Configure custom superuser credentials via `DJANGO_SUPERUSER_*` environment variables.
- [x] Verify SSL redirect is active (`SECURE_SSL_REDIRECT=True` is enabled when `DEBUG=False`).
- [x] Confirm `CSRF_TRUSTED_ORIGINS` includes your custom domain with `https://`.
- [x] Health check endpoint is available at `/health/` for uptime monitoring.
