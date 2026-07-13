#!/usr/bin/env bash
# build.sh — Render build script
# Render runs this automatically before starting the web service.
set -o errexit   # exit on first error

pip install --upgrade pip
pip install -r requirements.txt

# Collect static files into STATIC_ROOT (staticfiles/)
python manage.py collectstatic --no-input

# Apply any pending database migrations
python manage.py migrate
