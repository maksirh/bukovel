from django.shortcuts import render, get_object_or_404

from .querysets import active_offers


def offer_list(request):
    context = {'offers': active_offers()}
    return render(request, 'offers/list.html', context)


def offer_detail(request, slug):
    offers = active_offers()
    offer = get_object_or_404(offers, slug=slug)
    other = offers.exclude(pk=offer.pk)[:3]
    context = {'offer': offer, 'other_offers': other}
    return render(request, 'offers/detail.html', context)
