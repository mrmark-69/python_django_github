from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .admin_mixins import ExportAsCsvMixin
from .models import Product, Order


class OrderInline(admin.TabularInline):
    model = Product.orders.through


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
    ]
    # list_display = "id", "name", "description", "price", "discount"
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
        ("Create options", {
            "fields":("created_by",),
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


# class ProductInline(admin.TabularInline):
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

# admin.site.register(Product, ProductAdmin)
