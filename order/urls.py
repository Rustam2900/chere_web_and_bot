from django.urls import path

from order.views import AddItemToCartView, ListItemsFromCardView, RemoveItemFromCartView, OrderCreateView, RemoveCart

urlpatterns = [
    path('create-order/', OrderCreateView.as_view(), name='order_create'),
    path('list-cart-items/', ListItemsFromCardView.as_view(), name='cart_item_list'),
    path('delete-cart/', RemoveCart.as_view(), name='cart_delete'),
    path('add-item-to-cart/<int:product_id>/', AddItemToCartView.as_view(), name='add_cart_item'),
    path('remove-item-from-cart/<int:product_id>/', RemoveItemFromCartView.as_view(), name='remove_cart_item'),
]

