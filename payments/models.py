from django.db import models

import secrets

from django.conf import settings

from orders.models import Order


# Create your models here.
class Transaction(models.Model):
    STATUS = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("refunding", "Refunding"),
        ("refunded", "Refunded"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments")
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name="payment", null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    ref = models.CharField(max_length=200, unique=True)
    date_initiated = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)
    status = models.CharField(max_length=100, choices=STATUS, default="Pending")

    class Meta:
        ordering = ("-date_initiated", )

    def __str__(self):
        return f"Payment {self.ref}"

    def save(self, *args, **kwargs):
        while not self.ref:
            self.ref = secrets.token_urlsafe(50)

        if not self.amount:
            self.amount = self.order.total_cost_with_shipping_with_discount()

        super().save(*args, **kwargs)
