from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

DJANGO_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
]

THIRD_PARTY_APPS = [
    'tinymce',
    'cloudinary_storage',
    'cloudinary',
]

LOCAL_APPS = [
    'apps.core',
    'apps.rooms',
    'apps.spa',
    'apps.restaurant',
    'apps.services',
    'apps.offers',
    'apps.bookings',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'config.middleware.ContentSecurityPolicyMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

DATABASES = {
    'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR}/db.sqlite3')
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'uk'
LANGUAGES = [
    ('uk', 'Українська'),
    ('en', 'English'),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
MODELTRANSLATION_DEFAULT_LANGUAGE = 'uk'
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'uk'
TIME_ZONE = 'Europe/Kyiv'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache',
    }
}

# ---------------------------------------------------------------------------
# Cloudinary — медіафайли (активний storage лише в prod через DEFAULT_FILE_STORAGE)
# ---------------------------------------------------------------------------
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME', default=''),
    'API_KEY':    env('CLOUDINARY_API_KEY',    default=''),
    'API_SECRET': env('CLOUDINARY_API_SECRET', default=''),
}

EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@zatyshnyi-dvir.com')
BOOKING_NOTIFY_EMAIL = env('BOOKING_NOTIFY_EMAIL', default='info@zatyshnyi-dvir.com')

# ---------------------------------------------------------------------------
# Unfold — тема адмін-панелі (сумісна з Python 3.14 / Django 5.x)
# ---------------------------------------------------------------------------
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    'SITE_TITLE': 'Затишний Двір',
    'SITE_HEADER': 'Затишний Двір',
    'SITE_SUBHEADER': 'Панель управління',
    'SITE_URL': '/',
    'SITE_SYMBOL': 'hotel',
    'SHOW_HISTORY': True,
    'SHOW_VIEW_ON_SITE': True,
    'COLORS': {
        'primary': {
            '50': '250 245 235',
            '100': '245 235 215',
            '200': '235 215 180',
            '300': '220 190 140',
            '400': '200 160 90',
            '500': '180 135 60',
            '600': '155 110 40',
            '700': '125 85 25',
            '800': '95 65 15',
            '900': '70 45 10',
            '950': '45 28 5',
        },
    },
    'SIDEBAR': {
        'show_search': True,
        'show_all_applications': True,
        'navigation': [
            {
                'title': _('Контент сайту'),
                'separator': True,
                'items': [
                    {
                        'title': 'Налаштування сайту',
                        'icon': 'settings',
                        'link': '/admin/core/sitesettings/',
                    },
                    {
                        'title': 'Слайди Hero',
                        'icon': 'image',
                        'link': '/admin/core/heroslide/',
                    },
                    {
                        'title': 'Статистика на головній',
                        'icon': 'bar_chart',
                        'link': '/admin/core/statitem/',
                    },
                ],
            },
            {
                'title': _('Номери'),
                'separator': True,
                'items': [
                    {
                        'title': 'Типи номерів',
                        'icon': 'bed',
                        'link': '/admin/rooms/roomtype/',
                    },
                    {
                        'title': 'Фото номерів',
                        'icon': 'photo_library',
                        'link': '/admin/rooms/roomimage/',
                    },
                ],
            },
            {
                'title': _('SPA'),
                'separator': True,
                'items': [
                    {
                        'title': 'Розклад та опис SPA',
                        'icon': 'schedule',
                        'link': '/admin/spa/spaschedule/',
                    },
                    {
                        'title': 'Зони SPA',
                        'icon': 'spa',
                        'link': '/admin/spa/spazone/',
                    },
                    {
                        'title': 'Пакети SPA',
                        'icon': 'sell',
                        'link': '/admin/spa/spapackage/',
                    },
                    {
                        'title': 'Галерея SPA',
                        'icon': 'photo_library',
                        'link': '/admin/spa/spagallery/',
                    },
                ],
            },
            {
                'title': _('Ресторан'),
                'separator': True,
                'items': [
                    {
                        'title': 'Інфо про ресторан',
                        'icon': 'restaurant',
                        'link': '/admin/restaurant/restaurantinfo/',
                    },
                    {
                        'title': 'Розділи меню',
                        'icon': 'menu_book',
                        'link': '/admin/restaurant/menusection/',
                    },
                    {
                        'title': 'Позиції меню',
                        'icon': 'lunch_dining',
                        'link': '/admin/restaurant/menuitem/',
                    },
                ],
            },
            {
                'title': _('Послуги та акції'),
                'separator': True,
                'items': [
                    {
                        'title': 'Послуги',
                        'icon': 'room_service',
                        'link': '/admin/services/service/',
                    },
                    {
                        'title': 'Спецпропозиції',
                        'icon': 'local_offer',
                        'link': '/admin/offers/specialoffer/',
                    },
                ],
            },
            {
                'title': _('Бронювання'),
                'separator': True,
                'items': [
                    {
                        'title': 'Заявки на бронювання',
                        'icon': 'calendar_month',
                        'link': '/admin/bookings/bookingrequest/',
                    },
                ],
            },
            {
                'title': _('Адміністратори'),
                'separator': True,
                'items': [
                    {
                        'title': 'Користувачі',
                        'icon': 'person',
                        'link': '/admin/auth/user/',
                    },
                    {
                        'title': 'Групи',
                        'icon': 'group',
                        'link': '/admin/auth/group/',
                    },
                ],
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# TinyMCE — rich-text редактор
# ---------------------------------------------------------------------------
TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'menubar': False,
    'plugins': 'advlist autolink lists link image charmap preview anchor '
               'searchreplace visualblocks code fullscreen insertdatetime '
               'media table paste help wordcount',
    'toolbar': (
        'undo redo | formatselect | bold italic underline | '
        'alignleft aligncenter alignright alignjustify | '
        'bullist numlist outdent indent | link | removeformat | code | help'
    ),
    'content_style': 'body { font-family: Arial, sans-serif; font-size: 14px; }',
}
