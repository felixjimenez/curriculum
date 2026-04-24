#!/usr/bin/env bash
# Build script ejecutado por Render en cada deploy.
# Configurar una sola vez en Render → Settings → Build Command: ./build.sh
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
