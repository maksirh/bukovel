from django.db.models import Q
from django.utils import timezone

from .models import SpecialOffer


def active_offers():
    today = timezone.localdate()
    return (
        SpecialOffer.objects.filter(is_active=True)
        .filter(Q(valid_from__isnull=True) | Q(valid_from__lte=today))
        .filter(Q(valid_to__isnull=True) | Q(valid_to__gte=today))
    )
