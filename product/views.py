from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.throttling import UserRateThrottle

from product.models import Product, WebOrder, Action
from product.serializers import ProductHomeListSerializer, WebOrderSerializer, ProductListSerializer, ActionSerializer, ActionProductSerializer


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
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    throttle_classes = []



class ActionProductsAPIView(RetrieveAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionProductSerializer
