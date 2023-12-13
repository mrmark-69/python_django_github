from csv import DictReader
from io import TextIOWrapper

from django.contrib import admin
from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

from .admin_mixins import ExportAsCsvMixin
from .forms import CSVImportForm
from .models import Product, Order, ProductImage


class OrderInline(admin.TabularInline):
    model = Product.orders.through


class ProductInlineImage(admin.StackedInline):
    model = ProductImage


@admin.action(description="Archive products")
def mark_archived(model_admin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description="Unarchive products")
def mark_unarchived(model_admin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCsvMixin):
    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv",
    ]
    inlines = [
        OrderInline,
        ProductInlineImage,
    ]
    list_display = "id", "name", "description_short", "price", "discount", "archived",
    list_display_links = "id", "name",
    ordering = "id", "name",
    search_fields = "name", "description", "id"
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
            "classes": ("collapse", "wide"),
        }),
        ("Images", {
            "fields": ("preview",),
        }),
        ("Create options", {
            "fields": ("created_by",),
            "classes": ("collapse",)
        }),
        ("Extra options", {"fields": ("archived",),
                           "classes": ("collapse",),
                           "description": "Extra options. Field 'archived' is for soft delete.",
                           }),
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) > 48:
            return f"{obj.description[:48]}..."
        return obj.description

    change_list_template = "shopapp/products_changelist.html"

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context, status=400)

        csv_file = TextIOWrapper(
            form.files["csv_file"].file,
            encoding=request.encoding,
        )
        reader = DictReader(csv_file)

        products = [
            Product(**row)
            for row in reader
        ]
        Product.objects.bulk_create(products)
        self.message_user(request, "Data from CSV was imported.")
        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-products-csv/",
                self.import_csv,
                name="import_products_csv",
            ),
        ]
        return new_urls + urls


class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = "delivery_address", "promocode", "created_at", "user_verbose"

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    change_list_template = "shopapp/orders_changelist.html"

    @transaction.atomic
    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context, status=400)

        csv_file = TextIOWrapper(
            form.files["csv_file"].file,
            encoding=request.encoding,
        )
        reader = DictReader(csv_file)

        for row in reader:
            order = Order(
                delivery_address=row['delivery_address'],
                promocode=row['promocode'],
                user_id=row['user_id']
            )
            order.save()

            products_pk = [int(pk) for pk in row['products'].split(', ')]

            order.products.set(products_pk)

        self.message_user(request, "Data from CSV was successfully loaded")
        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-orders-csv/",
                self.import_csv,
                name="import_orders_csv",
            ),
        ]
        return new_urls + urls
