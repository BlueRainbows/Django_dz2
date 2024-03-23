from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='BlueberryRainbows@yandex.ru',
            first_name='admin',
            last_name='BlueRain',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('Ad.Dam03')
        user.save()
