from django.urls import path

from product.views import ProductHomeListView, WebOrderCreateAPIView, ProductListView, DiscountListView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('home/', ProductHomeListView.as_view(), name='home'),
    path('web-order/', WebOrderCreateAPIView.as_view(), name='web-order'),
    path('discount/', DiscountListView.as_view(), name='discount')
    # path('discount-create/', DiscountCreateAPIView.as_view(), name='discount-create')

]
