#!/usr/bin/env bash
# Початкове налаштування: міграції, адмін, seed-дані.
#
# Локально:
#   ./scripts/setup.sh
#   ./scripts/setup.sh --clear          # очистити контент і заповнити заново
#
# Render Shell (prod):
#   export DJANGO_SETTINGS_MODULE=config.settings.prod
#   ./scripts/setup.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -f "$ROOT/.venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT/.venv/bin/activate"
elif [[ -f "$ROOT/venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT/venv/bin/activate"
fi

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.dev}"

echo ""
echo "==> Міграції"
python manage.py migrate --noinput

echo ""
echo "==> Таблиця кешу (rate limiting)"
python manage.py createcachetable 2>/dev/null || true

echo ""
echo "==> Адмін (admin / admin)"
python manage.py setup_admin

echo ""
echo "==> Seed-дані (тексти + зображення з hotel_images/)"
python manage.py seed_db "$@"

echo ""
echo "✅ Готово!"
echo "   Сайт:  http://127.0.0.1:8000/"
echo "   Адмін: http://127.0.0.1:8000/admin/  (admin / admin)"
echo ""
