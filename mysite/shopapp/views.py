from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from timeit import default_timer
from django.utils import timezone



def shop_index(request: HttpRequest):
    products = [
        ('Laptop', 1999),
        ('Desktop', 2999),
        ('Smartphone', 999),
    ]
    context = {
        "time_now": timezone.now(),
        "time_running": default_timer(),
        "products": products,
        "header": "hello shop index",
    }
    return render(request, 'shopapp/shop-index.html', context=context)
