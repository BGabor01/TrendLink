#!/bin/sh

set -e

echo "===================== Migration session started ====================="
python manage.py makemigrations
python manage.py migrate
echo "===================== Migration session finished ====================="

echo "===================== Health check session started ====================="
python manage.py health_check
echo "===================== Health check session finished ====================="

pytest

python manage.py collectstatic --no-input

echo "===================== Starting application ====================="
exec "$@"