from rest_framework.serializers import ModelSerializer

from shopapp.models import Product, Order


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "pk", "name", "price"


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
