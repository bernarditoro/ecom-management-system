from django.db import models

from shop.models import Product, ProductColour

from django.conf import settings

from coupons.models import Coupon

from django.urls import reverse

from decimal import Decimal

from shipping.models import ShippingFee


# Create your models here.
class Order(models.Model):
    STATUS = (
        ("new", "New"),  # Recorded but not paid for
        ("accepted", "Accepted"),
        ("dispatched", "Dispatched"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    DELIVERY = (
        ("pickup", "Store Pickup"),
        ("dispatch", "Door Delivery"),
    )

    PAYMENT_METHOD = (
        ("cash", "Cash Payment"),
        ("bank", "Bank Transfer"),
        ("card", "Card Payment"),
    )

    order_number = models.CharField(max_length=20, null=True)
    ordered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="orders")
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default="new")
    amount_paid = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(null=True, max_length=50, choices=PAYMENT_METHOD,
                                      help_text="How the user paid for the order")
    payment_receipt = models.FileField(null=True, blank=True, upload_to="PaymentReceipts")  # If the user manually paid
    dispatched = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delivery_method = models.CharField(max_length=30, help_text="Delivery method", choices=DELIVERY, default="pickup")
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_address = models.CharField(max_length=300, null=True)
    sent_order_mail = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Order {self.order_number}"

    def save(self, *args, **kwargs):
        try:
            if not self.amount_paid:
                self.amount_paid = self.total_cost_with_shipping_with_discount()
        except:
            pass

        try:
            user_city = self.ordered_by.profile.city

            shipping = ShippingFee.objects.get(city=user_city)

            self.shipping_fee = shipping.fee
        except:
            pass

        super().save(*args, **kwargs)

    def number_of_items(self):
        return self.items.all().count()

    def total_cost(self):
        return sum(item.cost() for item in self.items.all())

    def order_discount(self):
        try:
            coupon_value = self.coupon.discount
            discount = (coupon_value * self.total_cost()) / 100
        except:
            discount = 0

        return discount

    def total_cost_with_shipping(self):
        return self.total_cost() + self.shipping_fee

    def total_cost_with_shipping_with_discount(self):
        return self.total_cost_with_shipping() - self.order_discount()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    colour = models.ForeignKey(ProductColour, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order Item {self.id}"

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price

        super().save(*args, **kwargs)

    def cost(self):
        return self.price * self.quantity
