#!/usr/bin/env bash
# Render start: один раз bootstrap, потім gunicorn.
set -euo pipefail

python manage.py bootstrap_once
exec gunicorn config.wsgi:application --workers 2 --timeout 120 --bind 0.0.0.0:"${PORT:-8000}"
