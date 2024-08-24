from django.urls import path

from users.views import UserRegistrationAPIView, UserLoginAPIView, UserProfileAPIView

urlpatterns = [
    path('registration/', UserRegistrationAPIView.as_view(), name='registration'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
]
