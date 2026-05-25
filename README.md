# Zatyshnyi Dvir — Готель & SPA Буковель

Django-сайт преміум готелю+SPA+ресторану в Буковелі.

## Стек

- **Backend:** Django 5.2 + Python 3.13
- **Frontend:** HTML5, CSS (модульний, mobile-first, BEM), vanilla JS, HTMX
- **DB:** SQLite (dev) / PostgreSQL (prod)
- **Static:** WhiteNoise
- **Media (prod):** Cloudinary
- **Admin:** django-unfold + TinyMCE
- **i18n:** django-modeltranslation (uk/en)

## Локальний старт

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# відредагуй .env (SECRET_KEY, EMAIL тощо)
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_db
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/  
Адмінка: http://127.0.0.1:8000/admin/

## Структура apps/

| App | Відповідальність |
|-----|-----------------|
| `core` | SiteSettings, HeroSlide, About, Contacts |
| `rooms` | Типи номерів, зображення, фічі |
| `spa` | Зони SPA, розклад |
| `restaurant` | Меню, секції, інфо |
| `services` | Pets, kids, parking, ski room |
| `offers` | Спеціальні пропозиції |
| `bookings` | Форма-заявка, email, статуси |

## Тести

```bash
python manage.py test --settings=config.settings.test
```

## Деплой на Render

### Важливо: Start Command

Render за замовчуванням запускає `gunicorn app:app` (Flask-шаблон) — для Django це **неправильно**.

**Start Command** (Settings → bukovel → Start Command):

```bash
gunicorn config.wsgi:application --workers 2 --timeout 120 --bind 0.0.0.0:$PORT
```

**Build Command** (Settings → Build Command):

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput && python manage.py createcachetable && python manage.py bootstrap_once
```

`bootstrap_once` — автоматично один раз створює admin (`admin`/`admin`) і заповнює seed-дані. Повторні деплої пропускають цей крок.

**Environment** — обов'язково:

```
DJANGO_SETTINGS_MODULE=config.settings.prod
```

### Варіант A — Blueprint (рекомендовано)

1. Render → **New** → **Blueprint**
2. Підключити репозиторій — Render прочитає `render.yaml` автоматично

### Варіант B — ручний Web Service

1. Підключити GitHub-репозиторій
2. Вручну вставити **Start Command** і **Build Command** з блоків вище
3. Додати PostgreSQL і env vars (див. `.env.example`)

## Налаштування email

Для продакшну в `.env` або Render env vars:

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=app-password
BOOKING_NOTIFY_EMAIL=info@zatyshnyi-dvir.com
```

## Seed-дані

```bash
./scripts/setup.sh              # migrate + admin + seed (локально, завжди)
./scripts/setup.sh --clear      # очистити контент і заповнити заново
python manage.py bootstrap_once # один раз (як на Render при деплої)
python manage.py bootstrap_once --force  # примусово перезаповнити
```

На Render `bootstrap_once` викликається автоматично в Build Command після `migrate`.
Повторні push/deply **не перезаписують** контент — мітка зберігається в таблиці `SiteBootstrap`.

Контент редагується у файлах `apps/core/management/commands/_seed_data*.py`, зображення — у каталозі `hotel_images/`.
