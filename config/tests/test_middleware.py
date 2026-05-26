from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase, override_settings

from config.middleware import ContentSecurityPolicyMiddleware


class ContentSecurityPolicyMiddlewareTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = ContentSecurityPolicyMiddleware(lambda request: HttpResponse('ok'))

    @override_settings(DEBUG=False)
    def test_public_pages_get_csp(self):
        request = self.factory.get('/rooms/')
        response = self.middleware(request)
        self.assertIn('Content-Security-Policy', response)

    @override_settings(DEBUG=False)
    def test_admin_is_exempt_from_csp(self):
        request = self.factory.get('/admin/login/')
        response = self.middleware(request)
        self.assertNotIn('Content-Security-Policy', response)

    @override_settings(DEBUG=False)
    def test_tinymce_is_exempt_from_csp(self):
        request = self.factory.get('/tinymce/filebrowser/')
        response = self.middleware(request)
        self.assertNotIn('Content-Security-Policy', response)
