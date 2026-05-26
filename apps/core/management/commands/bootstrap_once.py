from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from apps.core.cloudinary_sync import cloudinary_configured, uses_cloudinary_storage
from apps.core.models import HeroSlide, SiteBootstrap


class Command(BaseCommand):
    help = (
        'Один раз створює admin (admin/admin) і заповнює seed_db. '
        'Повторні запуски пропускаються, поки не передано --force.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Примусово очистити контент і виконати seed_db --clear',
        )

    def handle(self, *args, **options):
        key = SiteBootstrap.KEY_INITIAL
        has_flag = SiteBootstrap.objects.filter(key=key).exists()
        has_content = HeroSlide.objects.exists()
        force = options['force']

        if not force:
            if has_flag and has_content:
                self.stdout.write(self.style.WARNING('⏭  Bootstrap вже виконано — пропуск.'))
                return
            if has_flag and not has_content:
                self.stdout.write(
                    self.style.WARNING('⚠  Мітка bootstrap є, але контент порожній — повторне заповнення.')
                )
                SiteBootstrap.objects.filter(key=key).delete()

        self.stdout.write(self.style.MIGRATE_HEADING('\n🚀  bootstrap_once — старт\n'))
        self.stdout.write(f'   Storage: {default_storage.__class__.__name__}')
        if cloudinary_configured():
            self.stdout.write(f'   Cloudinary: {settings.CLOUDINARY_STORAGE["CLOUD_NAME"]}')
        elif uses_cloudinary_storage(default_storage):
            self.stdout.write(
                self.style.WARNING('   ⚠  Cloudinary storage увімкнено, але env vars не задані')
            )

        call_command('setup_admin')

        if force:
            call_command('seed_db', '--clear')
        else:
            call_command('seed_db')

        if not HeroSlide.objects.exists():
            raise CommandError('seed_db не створив контент (HeroSlide порожній). Перевірте логи та Cloudinary.')

        SiteBootstrap.objects.update_or_create(key=key)

        self.stdout.write(self.style.SUCCESS('\n✅  bootstrap_once — завершено\n'))
