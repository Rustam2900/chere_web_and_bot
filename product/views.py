from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.throttling import UserRateThrottle

from product.models import Product, WebOrder, Discount
from product.serializers import ProductHomeListSerializer, WebOrderSerializer, ProductListSerializer, DiscountSerializer


class ProductHomeListView(ListAPIView):
    queryset = Product.objects.all()[:10]
    serializer_class = ProductHomeListSerializer


class WebOrderCreateAPIView(CreateAPIView):
    queryset = WebOrder.objects.all()
    serializer_class = WebOrderSerializer
    throttle_classes = [UserRateThrottle, ]


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class DiscountListView(ListAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    throttle_classes = []
