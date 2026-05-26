#!/usr/bin/env bash
# Завантаження фото з hotel_images/ на Cloudinary (без зміни текстів у БД).
#
# Локально (prod settings + .env Cloudinary):
#   ./scripts/sync_cloudinary.sh
#   ./scripts/sync_cloudinary.sh --force
#
# На Render викликається автоматично з scripts/start.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.prod}"

if [[ -f "$ROOT/.venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT/.venv/bin/activate"
elif [[ -f "$ROOT/venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT/venv/bin/activate"
fi

echo ""
echo "==> sync_cloudinary (DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE})"
echo ""

python manage.py sync_cloudinary "$@"

echo ""
echo "✅ Cloudinary sync завершено"
echo ""
