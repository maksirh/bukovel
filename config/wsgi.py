import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')

application = get_wsgi_application()

if settings.SECRET_KEY == 'build-only-insecure-key-not-for-runtime':
    raise ImproperlyConfigured('Set the SECRET_KEY environment variable in Render.')
