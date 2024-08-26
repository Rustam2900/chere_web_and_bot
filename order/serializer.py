from rest_framework import serializers

from order.models import CartItem, Order, OrderMinSum
from product.serializers import ProductListSerializer
from product.views import ProductHomeListView


class AddToCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("id", "user", "product", "quantity")
        read_only_fields = ("id", "user", "product", "quantity")


class RemoveCartItemViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("id",)


class CartItemListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ("id", "user", "product", "quantity")


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "address", "phone_number")


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "user", "phone_number", "status", "address", "location", "created_at")


class OrderMinSumSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMinSum
        fields = ("id", "min_order_sum")
