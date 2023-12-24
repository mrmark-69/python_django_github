from rest_framework import serializers

from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        # read_only_fields = ["archived"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        # read_only_fields = ["user"]
