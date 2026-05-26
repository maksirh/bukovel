#!/usr/bin/env bash
# Render start: швидкий gunicorn (порт), потім sync Cloudinary у фоні.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.prod}"
export PYTHONUNBUFFERED=1

echo "=========================================="
echo "  bukovel start.sh"
echo "  DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}"
echo "=========================================="

BOOTSTRAP_ARGS=()
if [[ "${BOOTSTRAP_FORCE:-}" == "1" ]]; then
  echo "  BOOTSTRAP_FORCE=1"
  BOOTSTRAP_ARGS+=(--force)
fi

echo "==> bootstrap_once"
python -u manage.py bootstrap_once "${BOOTSTRAP_ARGS[@]}"

echo "==> compilemessages (fallback)"
python -u manage.py compilemessages --ignore=.venv --ignore=venv 2>/dev/null || true

SYNC_ARGS=(--force)
if [[ "${CLOUDINARY_SYNC_SMART:-}" == "1" ]]; then
  echo "  CLOUDINARY_SYNC_SMART=1 — лише відсутні фото"
  SYNC_ARGS=()
fi
if [[ "${CLOUDINARY_SYNC_FORCE:-}" == "1" ]]; then
  SYNC_ARGS=(--force)
fi

PORT="${PORT:-8000}"
echo "==> gunicorn :${PORT}"
gunicorn config.wsgi:application \
  --workers 2 \
  --timeout 120 \
  --bind "0.0.0.0:${PORT}" \
  --access-logfile - \
  --error-logfile - &
GUNICORN_PID=$!

for _ in $(seq 1 15); do
  if (echo >/dev/tcp/127.0.0.1/"${PORT}") 2>/dev/null; then
    echo "==> gunicorn ready (PID ${GUNICORN_PID})"
    break
  fi
  sleep 1
done

echo "==> sync_cloudinary (background, hotel_images/ → Cloudinary)"
(
  python -u manage.py sync_cloudinary "${SYNC_ARGS[@]}" \
  && echo "==> sync_cloudinary OK" \
  || echo "==> sync_cloudinary FAILED (exit $?)"
) &
SYNC_PID=$!

echo "==> running: gunicorn=${GUNICORN_PID} sync=${SYNC_PID}"
wait "${GUNICORN_PID}"
