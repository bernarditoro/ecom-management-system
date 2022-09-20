from django.test import TestCase

from .models import Order, OrderItem

from shop.models import Product, ProductColour, ProductCategory

from django.contrib.auth import get_user_model

from coupons.models import Coupon

from datetime import datetime, timedelta

from shipping.models import Country, State, City, ShippingFee

from accounts.models import UserProfile


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

        cls.country = Country.objects.create(
            country="Test Country"
        )

        cls.state = State.objects.create(
            state="Test State",
            country=cls.country
        )

        cls.city = City.objects.create(
            city="Test City",
            state=cls.state
        )

        cls.shipping = ShippingFee.objects.create(
            city=cls.city,
            fee=500
        )

        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret"
        )

        cls.user_profile = UserProfile.objects.create(
            user=cls.user,
            city=cls.city
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
        self.assertEqual(self.order.shipping_fee, self.shipping.fee)
        self.assertEqual(self.user.profile.city, self.city)

    def test_order_item(self):
        self.assertEqual(self.order_item.price, self.product.price)
        self.assertEqual(self.order_item.cost(), 20000)
