from django.test import TestCase

from .models import Order, OrderItem

from shop.models import Product, ProductColour, ProductCategory

from django.contrib.auth import get_user_model

from coupons.models import Coupon

from datetime import datetime, timedelta


# Create your tests here.
class OrderTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = ProductCategory.objects.create(
            name="Footwears",
            slug="footwears",
            image=""
        )

        cls.colour = ProductColour.objects.create(
            colour="Blue"
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

        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret"
        )

        cls.coupon = Coupon.objects.create(
            code="TEST10",
            valid_from=datetime.now(),
            valid_to=datetime.now() + timedelta(days=3),
            discount=10
        )

        cls.order = Order.objects.create(
            order_number=12345,
            ordered_by=cls.user,
            shipping_fee=500,
            coupon=cls.coupon
        )

        cls.order_item = OrderItem.objects.create(
            order=cls.order,
            product=cls.product,
            quantity=2,
            colour=cls.colour
        )

    def test_order(self):
        self.assertEqual(str(self.order), "Order 12345")
        self.assertEqual(self.order.total_cost(), self.order_item.cost())
        self.assertEqual(self.order.number_of_items(), 1)
        self.assertEqual(self.order.order_discount(), 2000)
        self.assertEqual(self.order.total_cost_with_shipping(), 20500)
        self.assertEqual(self.order.total_cost_with_shipping_with_discount(), 18500)

    def test_order_item(self):
        self.assertEqual(self.order_item.price, self.product.price)
        self.assertEqual(self.order_item.cost(), 20000)
