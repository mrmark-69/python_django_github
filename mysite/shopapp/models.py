from django.db import models
from django.contrib.auth.models import User


def product_preview_directory_path(instance: "Product", filename: str) -> str:
    return f"products/product_{instance.pk}/preview/{filename}"


class Product(models.Model):
    class Meta:
        ordering = ["created_at", "price", "name"]
        # db_table = "tech_products"
        # verbose_name_plural = "products"

    name = models.CharField(max_length=100, verbose_name="Name of product")
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)

    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    return f"products/product_{instance.product.pk}/images/{filename}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=product_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)


class Order(models.Model):
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")
    receipt = models.FileField(null=True, upload_to='orders/receipts/')
