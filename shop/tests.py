from django.test import TestCase

from .models import ProductCategory, Product, ProductColour


# Create your tests here.
class ShopTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = ProductCategory.objects.create(
            name="Footwears",
            slug="footwears",
            image=""
        )

        cls.colour = ProductColour.objects.create(
            colour="Red"
        )

        cls.product = Product.objects.create(
            name="Luxury Footwear",
            slug="luxury-footwear",
            category=cls.category,
            stock=2,
            description="Nice Footwear",
            image="",
            price=10000
        )
        cls.product.colours.add(cls.colour)

    def test_product(self):
        self.assertEqual(str(self.product), self.product.name)
        self.assertEqual(self.product.colours.get(pk=self.colour.pk), self.colour)

