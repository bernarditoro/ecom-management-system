from django.test import TestCase

from orders.models import Order, OrderItem

from django.contrib.auth import get_user_model

from .models import Transaction

from shop.models import Product, ProductColour, ProductCategory


# Create your tests here.
class PaymentTests(TestCase):
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

        cls.order = Order.objects.create(
            order_number=12345,
            ordered_by=cls.user,
            shipping_fee=500,
        )

        cls.order_item = OrderItem.objects.create(
            order=cls.order,
            product=cls.product,
            quantity=2,
            colour=cls.colour
        )

        cls.payment = Transaction.objects.create(
            user=cls.user,
            order=cls.order,
        )

    def test_transaction(self):
        self.assertEqual(self.payment.order.ordered_by, self.user)
        self.assertEqual(self.payment.amount, self.order.total_cost_with_shipping_with_discount())
