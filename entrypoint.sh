#!/bin/sh

echo "Waiting for PostgreSQL database..."
until python -c "import socket; s = socket.socket(); s.connect(('$DB_HOST', int('$DB_PORT')))" 2>/dev/null; do
    sleep 1
done
echo "PostgreSQL started successfully."

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000