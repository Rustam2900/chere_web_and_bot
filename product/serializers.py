from attr import attributes
from rest_framework import serializers

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
    class Meta:
        model = Action
        fields = ("title", "desc", "image", "percentage")


class ProductListSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    action = ActionSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ("id", "title", "price", "desc", "quantity", "attributes", "action")
