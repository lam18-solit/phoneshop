import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create superuser from environment variables if none exists'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        email = os.environ.get('DJANGO_ADMIN_EMAIL')
        password = os.environ.get('DJANGO_ADMIN_PASSWORD')

        if not email or not password:
            self.stdout.write('DJANGO_ADMIN_EMAIL or DJANGO_ADMIN_PASSWORD not set, skipping.')
            return

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write('Superuser already exists, skipping.')
            return

        User.objects.create_superuser(email=email, password=password)
        self.stdout.write(f'Superuser created: {email}')
