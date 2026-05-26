"""
Завантажує фото з hotel_images/ на Cloudinary для наявних записів БД.
Не чіпає тексти — лише ImageField.

Використання:
    python manage.py sync_cloudinary           # лише відсутні / биті URL
    python manage.py sync_cloudinary --force   # перезалити все
"""
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError

from apps.core.cloudinary_sync import cloudinary_configured, uses_cloudinary_storage
from apps.core.management.commands.seed_db import Command as SeedCommand


class Command(BaseCommand):
    help = 'Синхронізує зображення з hotel_images/ на Cloudinary (без зміни текстів у БД)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Перезалити всі фото, навіть якщо URL на Cloudinary вже працює',
        )

    def handle(self, *args, **options):
        if not uses_cloudinary_storage(default_storage):
            if settings.DEBUG:
                self.stdout.write(self.style.WARNING(
                    '⏭  sync_cloudinary — dev storage (FileSystem), пропуск.'
                ))
                return
            raise CommandError(
                'Prod storage не Cloudinary. Перевірте STORAGES у config/settings/prod.py'
            )

        if not cloudinary_configured():
            raise CommandError(
                'Cloudinary credentials не задані. '
                'Потрібні CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET'
            )

        seed = SeedCommand()
        seed.stdout = self.stdout
        seed.style = self.style
        seed.sync_all_images(smart=not options['force'], force=options['force'])

        if seed._images_fail and seed._images_ok == 0:
            raise CommandError(
                f'Жодне фото не завантажено ({seed._images_fail} помилок). '
                'Перевірте hotel_images/ та Cloudinary credentials.'
            )
