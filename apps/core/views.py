from django.shortcuts import render
from apps.core.models import SiteSettings, HeroSlide, StatItem
from apps.rooms.models import RoomType
from apps.spa.models import SpaZone, SpaSchedule
from apps.restaurant.models import RestaurantInfo
from apps.services.models import Service
from apps.offers.querysets import active_offers
from apps.bookings.forms import BookingForm


def home(request):
    context = {
        'hero_slides': HeroSlide.objects.filter(is_active=True),
        'stat_items': StatItem.objects.filter(is_active=True),
        'rooms': RoomType.objects.filter(is_active=True)[:6],
        'spa_zones': SpaZone.objects.all()[:4],
        'spa_schedule': SpaSchedule.load(),
        'restaurant_info': RestaurantInfo.load(),
        'services': Service.objects.filter(is_active=True),
        'offers': active_offers()[:3],
        'booking_form': BookingForm(),
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def contacts(request):
    return render(request, 'core/contacts.html')
