from typing import Sequence

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Order, Product


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk actions")
        result = Product.objects.filter(name__contains="Smartphone").update(created_by=2)
        print(result)
        # info = [
        #     ("Smartphone 1", 199),
        #     ("Smartphone 2", 299),
        #     ("Smartphone 2", 399),
        # ]
        # products = [
        #     Product(name=name, price=price)
        #     for name, price in info
        # ]
        # result = Product.objects.bulk_create(products)
        # for obj in result:
        #     print(obj)
        self.stdout.write("Done")
