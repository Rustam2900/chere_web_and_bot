from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.throttling import UserRateThrottle

from product.models import Product, WebOrder
from product.serializers import ProductHomeListSerializer, WebOrderSerializer, ProductListSerializer


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