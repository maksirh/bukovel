from .models import SiteSettings


def site_settings(request):
    settings_obj = SiteSettings.load()
    return {
        'site_settings': settings_obj,
    }
