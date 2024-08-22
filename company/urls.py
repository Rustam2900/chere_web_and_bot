from django.urls import path
from .views import BannerListView, AboutUsHomeView, AboutUsView, SocialMediaView, ContactWithUsView

urlpatterns = [
    path('banners/', BannerListView.as_view(), name='banner-list'),
    path('about-us/home/', AboutUsHomeView.as_view(), name='about-us-home'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('social-media/', SocialMediaView.as_view(), name='social-media'),
    path('contact-us', ContactWithUsView.as_view(), name='contact-us'),

]
