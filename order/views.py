from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from order.models import CartItem, Order, OrderMinSum
from order.serializer import AddItemToCartSerializer, ListItemsFromCardViewSerializer, RemoveItemFromCartViewSerializer, \
    OrderCreateSerializer, OrderListSerializer, OrderMinSumSerializer, RemoveCartSerializer
from product.models import Product


class AddItemToCartView(CreateAPIView):
    serializer_class = AddItemToCartSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product.objects.get(pk=kwargs.get('product_id'))
        if product.quantity <= 0:
            return Response({"error": "Извините, товар временно недоступен"}, status=status.HTTP_400_BAD_REQUEST)
        cart_items = CartItem.objects.filter(user=request.user, product=product, is_visible=True)
        if not cart_items.exists():
            CartItem.objects.create(user=request.user, product=product, quantity=1, is_visible=True)

        else:
            cart_item = cart_items.last()
            cart_item.quantity += 1
            cart_item.save()
        return Response({"status": "Вы добавили товар в корзину"}, status=status.HTTP_201_CREATED)


class RemoveItemFromCartView(RetrieveUpdateDestroyAPIView):
    serializer_class = RemoveItemFromCartViewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = []

    def get_queryset(self):
        qs = CartItem.objects.filter(user=self.request.user)
        return qs

    def destroy(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product_in_cart = CartItem.objects.filter(user=request.user, product=product_id).first()
        if product_in_cart.exists() is None:
            return Response({"В вашей корзине нет такого товара!"}, status=status.HTTP_404_NOT_FOUND)
        elif product_in_cart.quantity > 1:
            product_in_cart.quantity -= 1
            product_in_cart.save()
            return Response({"Количество товара уменьшено"}, status=status.HTTP_200_OK)
        else:
            product_in_cart.delete()
        return Response({"Товар удален из вашей корзины"}, status=status.HTTP_200_OK)


class ListItemsFromCardView(ListAPIView):
    serializer_class = ListItemsFromCardViewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = []

    def get_queryset(self):
        user = self.request.user
        qs = CartItem.objects.filter(user=user, is_visible=True)
        return qs


class RemoveCart(CreateAPIView):
    serializer_class = RemoveCartSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = []

    def post(self, request, *args, **kwargs):
        qs = CartItem.objects.filter(user=request.user, is_visible=True).all()
        if qs:
            qs.delete()
            return Response({"message": _("All items from the cart have been removed")}, status=status.HTTP_200_OK)
        return Response({"message": _("Your cart is empty")}, status=status.HTTP_404_NOT_FOUND)


class OrderCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = []
    serializer_class = OrderCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderListSerializer

    def get_queryset(self):
        qs = Order.objects.filter(user=self.request.user).all()
        return qs

    def create(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user,is_visible=True)
        if not cart_items.exists():
            return Response({"error": "Ваша корзина пуста. Добавьте товары перед оформлением заказа."},
                            status=status.HTTP_404_NOT_FOUND)
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                address=request.data.get('address'),
                phone_number=request.data.get('phone_number'),
                status=Order.OrderStatus.CREATED,
                total_price=total_price
            )

            for item in cart_items:
                item.order = order
                item.is_visible = False
                item.save()
        return Response({"status": "Заказ успешно создан"}, status=status.HTTP_201_CREATED)


class OrderCancelView(RetrieveUpdateDestroyAPIView):
    pass


class OrderMinSumView(ListAPIView):
    serializer_class = OrderMinSumSerializer
    throttle_classes = []
    queryset = OrderMinSum.objects.all()
