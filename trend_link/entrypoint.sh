#!/bin/sh

set -e

echo "===================== Migration session started ====================="
python manage.py makemigrations user
python manage.py migrate
echo "===================== Migration session finished ====================="

pytest

python manage.py collectstatic --no-input

echo "===================== Starting application ====================="
exec "$@"