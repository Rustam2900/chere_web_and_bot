from django.urls import path

from order.views import AddItemToCartView, ListItemsFromCardView, RemoveItemFromCartView, OrderCreateView, RemoveCart, \
    OrderHistoryListView, OrderCancelView, OrderMinSumView

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('order-list/', OrderHistoryListView.as_view(), name='order_history_list'),
    path('<int:order_id>/order-cancel/', OrderCancelView.as_view(), name='order_cancel'),
    path('order-min-sum/', OrderMinSumView.as_view(), name='order_min_sum'),
    path('list-cart-items/', ListItemsFromCardView.as_view(), name='cart_item_list'),
    path('delete-cart/', RemoveCart.as_view(), name='cart_delete'),
    path('add-item-to-cart/<int:product_id>/', AddItemToCartView.as_view(), name='add_cart_item'),
    path('remove-item-from-cart/<int:product_id>/', RemoveItemFromCartView.as_view(), name='remove_cart_item'),
]
