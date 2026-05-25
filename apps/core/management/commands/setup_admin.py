from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Створити або оновити суперкористувача (за замовчуванням admin/admin)'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin')
        parser.add_argument('--password', default='admin')
        parser.add_argument('--email', default='admin@example.com')

    def handle(self, *args, **options):
        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username=options['username'],
            defaults={
                'email': options['email'],
                'is_staff': True,
                'is_superuser': True,
            },
        )
        user.email = options['email']
        user.is_staff = True
        user.is_superuser = True
        user.set_password(options['password'])
        user.save()

        action = 'створено' if created else 'оновлено'
        self.stdout.write(
            self.style.SUCCESS(
                f'✔  Адмін {options["username"]} {action} (пароль: {options["password"]})'
            )
        )
