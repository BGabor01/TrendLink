#!/bin/sh

set -e

echo "===================== Migration session started ====================="
python manage.py makemigrations
python manage.py migrate
echo "===================== Migration session finished ====================="

python manage.py collectstatic --no-input

echo "===================== Starting application ====================="
exec "$@"