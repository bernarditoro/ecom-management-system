from django.test import TestCase

from .models import Coupon

from datetime import date


class CouponTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.coupon = Coupon.objects.create(
            code="TESTCODE",
            valid_from=date.today(),
            valid_to=date(2022, 10, 1),
            discount=10,
        )

    def test_coupon(self):
        self.assertEqual(self.coupon.code, "TESTCODE")
        self.assertEqual(self.coupon.valid_from, date.today())
        self.assertEqual(self.coupon.valid_to, date(2022, 10, 1))
        self.assertEqual(self.coupon.discount, 10)
        self.assertEqual(str(self.coupon), "TESTCODE (10% discount)")

