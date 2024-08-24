from django.urls import path

from order.views import AddCartItemView, CartItemListView, RemoveCartItemView, OrderCreateView

urlpatterns = [
    path('cart-item-list', CartItemListView.as_view(), name='cart_item_list'),
    path('add-cart/<int:product_id>/', AddCartItemView.as_view(), name='add_cart_item'),
    path('remove-cart-item/<int:product_id>/', RemoveCartItemView.as_view(), name='remove_cart_item'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
]
