"""
This module contains various sets of views.

Different views for an online store: by product, order, etc.
"""

import os
import logging
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        UserPassesTestMixin)
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import Group, User
from timeit import default_timer

from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from .forms import OrderForm, GroupForm, ConfirmForm, ProductForm, ProductUpdateForm
from .models import Product, Order, ProductImage
from .serializers import ProductSerializer, OrderSerializer

log = logging.getLogger(__name__)


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 899),
        ]
        context = {
            "time_now": timezone.now(),
            "time_running": default_timer(),
            "products": products,
            "header": "hello shop index",
            "items": 4,
        }
        log.debug("Products for shop index: %s", products)
        log.info("Rendering shop index")
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = "shopapp/product-details.html"
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


@extend_schema(description='Product views CRUD')
class ProductViewSet(ModelViewSet):
    """
    A set of views for actions on a Product
    complete CRUD for product entities.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter
    ]
    search_fields = [  # Поля фильтрации для SearchFilter
        "name",
        "description",
    ]
    ordering_fields = [  # Поля фильтрации для OrderingFilter
        "pk",
        "price",
        "discount"
    ]

    @extend_schema(
        summary="Get one product by ID",
        description="Retrieves **product**, returns 404 if not found",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Empty response, product by id not found."),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class ProductsListView(ListView):
    template_name = 'shopapp/products-list.html'
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)



class ProductCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        user = self.request.user
        return self.request.user.is_superuser or user.has_perm('shopapp.add_product')

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.created_by = self.request.user
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        user = self.request.user
        product = self.get_object()
        return user.is_superuser or user.has_perm('shopapp.change_product') or product.created_by == user

    model = Product
    form_class = ProductUpdateForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)

        images_to_delete = form.cleaned_data.get('images_to_delete', [])

        for image_id in images_to_delete:
            image = ProductImage.objects.filter(id=image_id.pk).first()
            if image:
                file_path = f"./uploads/{image.image}"
                try:
                    os.remove(file_path)
                except OSError as e:
                    print(f"Ошибка удаления файла: {e}")
                image.delete()

        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )

        return response


class ProductArchiveView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        user = self.request.user
        product = self.get_object()
        return user.is_superuser or user.has_perm('shopapp.change_product') or product.created_by == user

    model = Product
    form_class = ConfirmForm
    success_url = reverse_lazy("shopapp:products_list")
    template_name_suffix = "_confirm_archive"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ProductDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by("pk").all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,
            }
            for product in products
        ]

        return JsonResponse({"products": products_data})


class OrdersViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter
    ]
    filterset_fields = [  # Поля фильтрации для DjangoFilterBackend
        "delivery_address",
        "promocode",
        "created_at",
        "user",
        "products"
    ]
    ordering_fields = [  # Поля фильтрации для OrderingFilter
        "pk",
        "created_at"
    ]


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderDetailView(LoginRequiredMixin, DetailView):
    # permission_required = "shopapp.view_order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('shopapp.add_order')

    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("shopapp:orders_list")


class OrderUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('shopapp.change_order')

    model = Order
    form_class = OrderForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk},
        )


class OrderDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('shopapp.change_order')

    model = Order
    success_url = reverse_lazy("shopapp:orders_list")
    form_class = ConfirmForm


class OrdersExportView(UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by("pk").all()
        orders_data = [
            {"pk": order.pk,
             "delivery_address": order.delivery_address,
             "promocode": order.promocode,
             "user": order.user.pk,
             "products": [product.pk for product in order.products.all()]
             }
            for order in orders
        ]
        return JsonResponse({"orders": orders_data})
