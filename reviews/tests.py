from django.test import TestCase

from shop.models import Product, ProductCategory

from .models import Review

from django.contrib.auth import get_user_model


# Create your tests here.
class ReviewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = ProductCategory.objects.create(
            name="Footwears",
            slug="footwears",
            image=""
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

        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret"
        )

        cls.review = Review.objects.create(
            product=cls.product,
            user=cls.user,
            subject="Test Subject",
            review="This is a test review",
            rating=9
        )

    def test_review(self):
        self.assertEqual(str(self.review), "Test Subject")
        self.assertEqual(self.review.get_rating_percentage(), 90)
        self.assertEqual(self.review.product, self.product)
        self.assertEqual(self.review.user, self.user)
