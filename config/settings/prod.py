import os
from .base import *  # noqa

DEBUG = False

# ---------------------------------------------------------------------------
# Hosts — Render hostname + опційний власний домен з ALLOWED_HOSTS
# ---------------------------------------------------------------------------
_render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
_hosts = env.list('ALLOWED_HOSTS', default=[])
if _render_host and _render_host not in _hosts:
    _hosts.append(_render_host)
ALLOWED_HOSTS = _hosts

CSRF_TRUSTED_ORIGINS = [
    f'https://{h}' for h in ALLOWED_HOSTS if h and not h.startswith('.')
]

# ---------------------------------------------------------------------------
# SSL — Render завершує TLS на проксі, тому redirect робить він, не Django.
# W008 заглушено навмисно: SECURE_SSL_REDIRECT не потрібен за проксі.
# ---------------------------------------------------------------------------
SILENCED_SYSTEM_CHECKS = ['security.W008']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# ---------------------------------------------------------------------------
# Cloudinary — зберігання медіафайлів
# ---------------------------------------------------------------------------
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
