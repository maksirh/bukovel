from django.core.cache import cache

BOOKING_RATE_LIMIT = 5
BOOKING_RATE_PERIOD = 3600


def get_client_ip(request) -> str | None:
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def is_booking_rate_limited(request) -> bool:
    ip = get_client_ip(request)
    if not ip:
        return False
    key = f'booking_rate:{ip}'
    return cache.get(key, 0) >= BOOKING_RATE_LIMIT


def increment_booking_rate_limit(request) -> None:
    ip = get_client_ip(request)
    if not ip:
        return
    key = f'booking_rate:{ip}'
    count = cache.get(key, 0)
    cache.set(key, count + 1, BOOKING_RATE_PERIOD)
