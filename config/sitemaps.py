from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.offers.querysets import active_offers
from apps.rooms.models import RoomType
from apps.services.models import Service


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'home',
            'about',
            'contacts',
            'room_list',
            'spa',
            'restaurant',
            'service_list',
            'offer_list',
            'booking',
        ]

    def location(self, item):
        return reverse(item)


class RoomSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return RoomType.objects.filter(is_active=True)

    def lastmod(self, obj):
        return None


class ServiceSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Service.objects.filter(is_active=True)


class OfferSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return active_offers()
