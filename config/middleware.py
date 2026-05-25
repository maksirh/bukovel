from django.conf import settings


class ContentSecurityPolicyMiddleware:
    """Prod-only CSP compatible with HTMX, Google Fonts and Cloudinary."""

    POLICY = (
        "default-src 'self'; "
        "script-src 'self' https://unpkg.com; "
        "style-src 'self' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https://res.cloudinary.com; "
        "connect-src 'self'; "
        "frame-src 'self' https://www.google.com https://maps.google.com; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not settings.DEBUG:
            response['Content-Security-Policy'] = self.POLICY
        return response
