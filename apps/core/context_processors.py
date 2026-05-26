from django.conf import settings
from django.urls import reverse
from django.utils.translation import override

from .models import SiteSettings


def site_settings(request):
    settings_obj = SiteSettings.load()
    return {
        'site_settings': settings_obj,
    }


def language_urls(request):
    """URL поточної сторінки для кожної мови (UK — без префікса, EN — /en/...)."""
    query = request.META.get('QUERY_STRING', '') if request else ''
    fallback = request.path if request else '/'
    urls = {code: fallback for code, _ in settings.LANGUAGES}

    match = getattr(request, 'resolver_match', None) if request else None
    if not match or not match.view_name:
        return {'language_urls': urls}

    for code, _ in settings.LANGUAGES:
        with override(code):
            url = reverse(match.view_name, args=match.args, kwargs=match.kwargs)
            if query:
                url = f'{url}?{query}'
            urls[code] = url

    return {'language_urls': urls}
