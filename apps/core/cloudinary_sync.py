"""Перевірка та синхронізація зображень з hotel_images/ на Cloudinary."""
from __future__ import annotations

import urllib.error
import urllib.request

from django.conf import settings


def cloudinary_configured() -> bool:
    return bool(settings.CLOUDINARY_STORAGE.get('CLOUD_NAME'))


def uses_cloudinary_storage(storage) -> bool:
    return 'cloudinary' in storage.__class__.__module__.lower()


def image_url_on_cloudinary(url: str) -> bool:
    return 'res.cloudinary.com' in url or 'cloudinary.com' in url


def image_url_reachable(url: str, timeout: int = 8) -> bool:
    if not url:
        return False
    try:
        request = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def needs_cloudinary_upload(image_field) -> bool:
    """True якщо поле порожнє, URL не Cloudinary, або файл на Cloudinary відсутній (404)."""
    if not image_field or not image_field.name:
        return True
    url = image_field.url
    if not image_url_on_cloudinary(url):
        return True
    return not image_url_reachable(url)
