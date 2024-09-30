from django.template.defaultfilters import title
from django.test import TestCase
from django.urls import reverse

from common.models import Media
from product.models import Product


class ProductListTestsCase(TestCase):
    def setUp(self):
        for i in range(15):
            Product.objects.create(
                title=f"Product {i}",
                desc=f"Description of Product {i}",
                size=2,
                image=Media.objects.create(type=f".jpg", file='https://example.com/image1.jpg'),

            )

    def test_product_home_list(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
