from django.shortcuts import render
from .models import SpaZone, SpaSchedule, SpaPackage, SpaGallery


def spa_index(request):
    context = {
        'zones': SpaZone.objects.all(),
        'schedule': SpaSchedule.load(),
        'packages': SpaPackage.objects.order_by('order'),
        'gallery': SpaGallery.objects.order_by('order')[:9],
    }
    return render(request, 'spa/index.html', context)
