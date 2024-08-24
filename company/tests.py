from django.http.request import MediaType
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse

from common.models import Media
from company.models import Banner


class TestBannerListView(APITestCase):
    url = reverse('banner-list')

    def setUp(self):
        pass

    def test_success(self):
        banner1 = Banner.objects.create(title='banner1', subtitle='subtitle1')
        banner2 = Banner.objects.create(title='banner2', subtitle='subtitle2')
        media = Media.objects.create(type=Media.MediaType.IMAGE, file='banner1.jpg')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
