"""
Завантажує фото з hotel_images/ на Cloudinary для наявних записів БД.
Не чіпає тексти — лише ImageField.

Використання:
    python manage.py sync_cloudinary           # лише відсутні / биті URL
    python manage.py sync_cloudinary --force   # перезалити все
"""
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from apps.core.cloudinary_sync import cloudinary_configured, uses_cloudinary_storage
from apps.core.models import SiteBootstrap
from apps.core.management.commands.seed_db import Command as SeedCommand

SYNC_FLAG_KEY = 'cloudinary_images_synced'


class Command(BaseCommand):
    help = 'Синхронізує зображення з hotel_images/ на Cloudinary (без зміни текстів у БД)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Перезалити всі фото, навіть якщо URL на Cloudinary вже є',
        )
        parser.add_argument(
            '--verify',
            action='store_true',
            help='HEAD-перевірка кожного URL (повільно, не для start.sh)',
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
            self.stdout.write(self.style.ERROR(
                'Cloudinary credentials не задані '
                '(CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET).'
            ))
            return

        seed = SeedCommand()
        seed.stdout = self.stdout
        seed.style = self.style
        seed._verify_remote = options['verify']
        seed.sync_all_images(smart=not options['force'], force=options['force'])

        if seed._images_ok > 0 and seed._images_fail == 0:
            SiteBootstrap.objects.update_or_create(key=SYNC_FLAG_KEY)

        if seed._images_fail:
            self.stdout.write(self.style.WARNING(
                f'Завершено з помилками: ok={seed._images_ok}, fail={seed._images_fail}'
            ))
        if seed._images_ok == 0 and seed._images_fail > 0:
            self.stdout.write(self.style.ERROR(
                'Жодне фото не завантажено. Перевірте hotel_images/ та Cloudinary credentials.'
            ))
