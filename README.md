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

1. Підключити репозиторій до Render
2. Застосувати Blueprint з `render.yaml` або створити Web Service + PostgreSQL вручну
3. У Render Dashboard задати змінні:
   - `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
   - `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
   - `BOOKING_NOTIFY_EMAIL`
   - `ALLOWED_HOSTS` — ваш домен (напр. `zatyshnyi-dvir.com,www.zatyshnyi-dvir.com`)
4. Render автоматично додає `RENDER_EXTERNAL_HOSTNAME` до `ALLOWED_HOSTS`

Build-команда (вже в `render.yaml`):

```bash
pip install -r requirements.txt &&
python manage.py collectstatic --noinput &&
python manage.py migrate --noinput &&
python manage.py createcachetable
```

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
python manage.py seed_db          # ідемпотентне заповнення
python manage.py seed_db --clear  # очистити контент і заповнити заново
```

Зображення беруться з каталогу `hotel_images/`.
