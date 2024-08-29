from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.response import Response
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
        fields = ("id", "address", "phone_number", "cart_items")

    def validate_cart_items(self, value):
        user_cart_items = CartItem.objects.filter(user=self.context["request"].user, is_visible=True).all()
        for item_id in value:
            if item_id not in user_cart_items.values_list('id', flat=True):
                raise serializers.ValidationError(_(f"Товар с ID {item_id} не найден в корзине."))
        return value


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "user", "phone_number", "status", "address", "created_at", "order_number")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        cart_items = CartItem.objects.filter(user=self.context.get("request").user, order_id=instance.id).values()
        products = []
        for item in cart_items:
            product = {"id": item['product_id'], "quantity": item['quantity']}
            products.append(product)
        data["products"] = products
        return data

class OrderCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "user", "phone_number", "status", "address", "created_at", "order_number")
        read_only_fields = ("id", "user", "phone_number", "status", "address", "created_at", "order_number")


class OrderMinSumSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMinSum
        fields = ("id", "min_order_sum")
