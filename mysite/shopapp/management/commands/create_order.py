from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Create order")
        user = User.objects.first()
        order = Order.objects.get_or_create(
            delivery_address="Russkaya str 90",
            promocode="PROMO123",
            user=user,
        )
        self.stdout.write(f"Created order {order}")
