from attr import attributes
from django.db.models import Sum
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from common.serializers import MediaURLSerializer
from product.models import Product, WebOrder, ProductAttribute, Action


class ProductHomeListSerializer(serializers.ModelSerializer):
    image = MediaURLSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ("id", "title", "desc", "image")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["title"] = f"{instance.title} {instance.size}L"
        i_attributes = instance.attributes.first()
        if i_attributes is not None:
            data["desc"] = f"{instance.desc[:20]} {i_attributes.title} / {instance.size}L"
        else:
            data["desc"] = f"{instance.desc[:20]} {instance.size}L"
        return data


class WebOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebOrder
        fields = "__all__"


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ("title", "value")


class ActionSerializer(serializers.ModelSerializer):
    product = Product

    class Meta:
        model = Action
        fields = ("id", "title", "desc", "image", "percentage")


class ProductListSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    action = ActionSerializer(read_only=True)
    image = MediaURLSerializer(read_only=True)
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id", "title", "price", "discount_price", "desc", "quantity", "attributes", "action", "image",
            "final_price")

    def get_final_price(self, instance):
        if instance.action:
            discount_percentage = instance.action.percentage
            return instance.price - (instance.price * discount_percentage / 100)
        return instance.price

    def to_representation_(self, instance):
        data = super().to_representation_(instance)
        data["title"] = f"{instance.title} {instance.size}L"
        i_attributes = instance.attributes.first()
        if i_attributes is not None:
            data["desc"] = f"{instance.desc[:20]} {i_attributes.title} / {instance.size}L"
        else:
            data["desc"] = f"{instance.desc[:20]} {instance.size}L"
        return data


class ActionProductSerializer(serializers.ModelSerializer):
    image = MediaURLSerializer(read_only=True)
    products = ProductListSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Action
        fields = ("title", "desc", "image", "percentage","products", "total_price")


    def get_total_price(self, instance):
        total_product_price = instance.products.aggregate(total_price=Sum('price'))['total_price']
        discount_price = total_product_price - total_product_price * instance.percentage / 100
        return discount_price