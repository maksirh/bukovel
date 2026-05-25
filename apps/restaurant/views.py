from django.shortcuts import render
from django.db.models import Prefetch
from .models import RestaurantInfo, MenuSection, MenuItem, RestaurantPhoto


def restaurant_index(request):
    active_items = Prefetch(
        'items',
        queryset=MenuItem.objects.filter(is_active=True).order_by('order'),
        to_attr='active_items',
    )
    sections = (
        MenuSection.objects
        .prefetch_related(active_items)
        .filter(items__is_active=True)
        .distinct()
        .order_by('order')
    )
    context = {
        'info': RestaurantInfo.load(),
        'sections': sections,
        'photos': RestaurantPhoto.objects.all(),
    }
    return render(request, 'restaurant/index.html', context)
