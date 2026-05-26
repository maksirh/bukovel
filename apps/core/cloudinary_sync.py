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


def image_url_reachable(url: str, timeout: int = 5) -> bool:
    if not url:
        return False
    try:
        request = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def needs_cloudinary_upload(image_field, *, verify_remote: bool = False) -> bool:
    """
    Чи потрібен upload.

    verify_remote=False (за замовчуванням): без HTTP — швидко на старті Render.
    verify_remote=True: додатково HEAD-перевірка (повільно, сотні запитів).
    """
    if not image_field or not image_field.name:
        return True
    url = image_field.url
    if not image_url_on_cloudinary(url):
        return True
    if verify_remote:
        return not image_url_reachable(url)
    return False
