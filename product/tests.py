from django.template.defaultfilters import title
from django.test import TestCase
from django.urls import reverse

from product.models import Product


class ProductListTestsCase(TestCase):
    def setUp(self):
        for i in range(15):
            Product.objects.create(
                title=f"Product {i}",
                desc=f"Description of Product {i}",

            )
    def test_product_home_list(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)