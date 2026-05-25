from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.core.models import SiteBootstrap


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

        if not options['force'] and SiteBootstrap.objects.filter(key=key).exists():
            self.stdout.write(self.style.WARNING('⏭  Bootstrap вже виконано — пропуск.'))
            return

        self.stdout.write(self.style.MIGRATE_HEADING('\n🚀  bootstrap_once — старт\n'))

        with transaction.atomic():
            call_command('setup_admin')

            if options['force']:
                call_command('seed_db', '--clear')
            else:
                call_command('seed_db')

            SiteBootstrap.objects.update_or_create(key=key)

        self.stdout.write(self.style.SUCCESS('\n✅  bootstrap_once — завершено\n'))
