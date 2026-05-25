import json
import os
import time
from pathlib import Path

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')

# #region agent log
def _debug_wsgi_log(message, data, hypothesis_id):
    try:
        base_dir = Path(__file__).resolve().parent.parent
        payload = {
            'sessionId': '4eb11a',
            'runId': os.environ.get('DEBUG_RUN_ID', 'pre-fix'),
            'hypothesisId': hypothesis_id,
            'location': 'config/wsgi.py',
            'message': message,
            'data': data,
            'timestamp': int(time.time() * 1000),
        }
        with open(base_dir / '.cursor/debug-4eb11a.log', 'a', encoding='utf-8') as fh:
            fh.write(json.dumps(payload, ensure_ascii=False) + '\n')
    except OSError:
        pass
# #endregion

_debug_wsgi_log(
    'wsgi startup',
    {
        'secret_key_in_environ': 'SECRET_KEY' in os.environ,
        'render': os.environ.get('RENDER'),
    },
    'H4',
)

application = get_wsgi_application()

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

if settings.SECRET_KEY == 'build-only-insecure-key-not-for-runtime':
    # #region agent log
    _debug_wsgi_log(
        'runtime blocked: placeholder SECRET_KEY',
        {'secret_key_in_environ': 'SECRET_KEY' in os.environ},
        'H4',
    )
    # #endregion
    raise ImproperlyConfigured('Set the SECRET_KEY environment variable in Render.')
