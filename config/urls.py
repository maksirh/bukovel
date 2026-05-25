from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from config.sitemaps import OfferSitemap, RoomSitemap, ServiceSitemap, StaticViewSitemap
from config.views import robots_txt

sitemaps = {
    'static': StaticViewSitemap,
    'rooms': RoomSitemap,
    'services': ServiceSitemap,
    'offers': OfferSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('apps.core.urls')),
    path('rooms/', include('apps.rooms.urls')),
    path('spa/', include('apps.spa.urls')),
    path('restaurant/', include('apps.restaurant.urls')),
    path('services/', include('apps.services.urls')),
    path('offers/', include('apps.offers.urls')),
    path('booking/', include('apps.bookings.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
