#!/bin/sh
# Production entrypoint: apply DB migrations, then serve the API with gunicorn.
set -e

python manage.py migrate --noinput

# Workers: rule of thumb 2*CPU+1; override with GUNICORN_WORKERS.
exec gunicorn django_calculators.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "${GUNICORN_WORKERS:-3}" \
    --timeout "${GUNICORN_TIMEOUT:-60}" \
    --access-logfile - \
    --error-logfile -
