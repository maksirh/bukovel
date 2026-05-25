from .base import *  # noqa

DEBUG = True

INTERNAL_IPS = ['127.0.0.1']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Показуємо email у консолі при дебазі
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
