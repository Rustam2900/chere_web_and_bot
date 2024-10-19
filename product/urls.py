from django.urls import path

from product.views import ProductHomeListView, WebOrderCreateAPIView, ProductListView, DiscountListView, ActionProductsAPIView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('home/', ProductHomeListView.as_view(), name='home'),
    path('web-order/', WebOrderCreateAPIView.as_view(), name='web-order'),
    path('discounts/', DiscountListView.as_view(), name='discount'),
    # path('discount-create/', DiscountCreateAPIView.as_view(), name='discount-create')
    path('discounts/<int:pk>/', ActionProductsAPIView.as_view(), name='order-action')
]
