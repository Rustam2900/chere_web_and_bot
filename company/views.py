from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from company.models import Banner, AboutUs, SocialMedia, ContactWithUs
from .serializers import BannerListSerializer, AboutUsHomeSerializer, AboutUsSerializer, SocialMediaSerializer, \
    ContactWithUsSerializer


class BannerListView(ListAPIView):
    serializer_class = BannerListSerializer
    throttle_classes = []

    def get_queryset(self):
        banners = Banner.objects.all()
        if not banners.exists():
            raise ValidationError('No banners found')
        return banners


class AboutUsHomeView(APIView):

    @extend_schema(responses=AboutUsHomeSerializer)
    def get(self, request, *args, **kwargs):
        about_us = AboutUs.objects.last()
        serializer = AboutUsHomeSerializer(about_us, context={'request': request})
        return Response(data=serializer.data)


class AboutUsView(APIView):

    @extend_schema(responses=AboutUsSerializer)
    def get(self, request, *args, **kwargs):
        about_us = AboutUs.objects.last()
        serializer = AboutUsSerializer(about_us, context={'request': request})
        return Response(serializer.data)


class ContactWithUsView(CreateAPIView):
    serializer_class = ContactWithUsSerializer
    queryset = ContactWithUs.objects.all()
    throttle_classes = [UserRateThrottle, ]


class SocialMediaView(ListAPIView):
    serializer_class = SocialMediaSerializer
    queryset = SocialMedia.objects.all()
