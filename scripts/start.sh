#!/usr/bin/env bash
# Render start: bootstrap (admin + seed + Cloudinary), потім gunicorn.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.prod}"

echo "=========================================="
echo "  bukovel start.sh — bootstrap + gunicorn"
echo "  DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}"
echo "=========================================="

BOOTSTRAP_ARGS=()
if [[ "${BOOTSTRAP_FORCE:-}" == "1" ]]; then
  echo "  BOOTSTRAP_FORCE=1 — примусовий seed"
  BOOTSTRAP_ARGS+=(--force)
fi

python manage.py bootstrap_once "${BOOTSTRAP_ARGS[@]}"

echo "=========================================="
echo "  sync_cloudinary — upload hotel_images/"
echo "=========================================="

SYNC_ARGS=()
if [[ "${CLOUDINARY_SYNC_FORCE:-}" == "1" ]]; then
  echo "  CLOUDINARY_SYNC_FORCE=1 — перезалити всі фото"
  SYNC_ARGS+=(--force)
fi

python manage.py sync_cloudinary "${SYNC_ARGS[@]}"

echo "=========================================="
echo "  bootstrap + sync завершено, старт gunicorn"
echo "=========================================="

exec gunicorn config.wsgi:application --workers 2 --timeout 120 --bind 0.0.0.0:"${PORT:-8000}"
