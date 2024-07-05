#!/bin/sh

set -e

echo "===================== Migration session started ====================="
python manage.py makemigrations
python manage.py migrate

echo "===================== Migration session finished ====================="
echo "===================== Starting application ====================="
exec "$@"