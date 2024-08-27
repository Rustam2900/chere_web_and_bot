from rest_framework import serializers

from order.models import CartItem, Order, OrderMinSum
from product.serializers import ProductListSerializer
from product.views import ProductHomeListView


class AddItemToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("id", "user", "product", "quantity")
        read_only_fields = ("id", "user", "product", "quantity")


class RemoveItemFromCartViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("id",)


class ListItemsFromCardViewSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ("id", "user", "product", "quantity")

class RemoveCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("id",)

class OrderCreateSerializer(serializers.ModelSerializer):
    cart_items = serializers.ListSerializer(child=serializers.IntegerField())
    class Meta:
        model = Order
        fields = ("id", "address", "phone_number")


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "user", "phone_number", "status", "address", "created_at")


class OrderMinSumSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMinSum
        fields = ("id", "min_order_sum")
