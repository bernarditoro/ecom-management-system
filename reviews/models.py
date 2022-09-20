from django.db import models

from shop.models import Product

from django.core.validators import MinValueValidator, MaxValueValidator

from django.conf import settings


# Create your models here.
class Review(models.Model):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviews", on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.DecimalField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                 decimal_places=1, max_digits=3)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    def get_rating_percentage(self):
        return self.rating / 10 * 100
