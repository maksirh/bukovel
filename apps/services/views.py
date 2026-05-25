from django.shortcuts import render, get_object_or_404
from .models import Service


def service_list(request):
    context = {'services': Service.objects.filter(is_active=True)}
    return render(request, 'services/list.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    other = Service.objects.filter(is_active=True).exclude(pk=service.pk)[:4]
    context = {'service': service, 'other_services': other}
    return render(request, 'services/detail.html', context)
