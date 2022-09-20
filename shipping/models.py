from django.db import models


class Country(models.Model):
    country = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self) -> str:
        return self.country


class State(models.Model):
    state = models.CharField(max_length=60)
    country = models.ForeignKey(Country, related_name="states", on_delete=models.CASCADE)

    class Meta:
        ordering = ("state", "country")

    def __str__(self):
        return f"{self.state}, {self.country}"


class City(models.Model):
    city = models.CharField(max_length=100)
    state = models.ForeignKey(State, related_name="cities", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.city}, {self.state}"


class ShippingFee(models.Model):
    city = models.OneToOneField(City, related_name="shipping", on_delete=models.CASCADE)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_duration = models.PositiveIntegerField(default=1,
                                                    help_text="The duration(in weeks) before it gets to the user")

    def __str__(self):
        return f"Shipping details: {self.city}"
