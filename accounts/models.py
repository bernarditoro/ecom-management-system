from django.db import models

from shipping.models import City

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser

from django.conf import settings


class Account(AbstractUser):
    name = models.CharField(default="", max_length=200)

    def __str__(self) -> str:
        return super().get_full_name()


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to="display_profiles", blank=True, null=True)
    home_address = models.TextField(null=True, blank=True)
    city = models.ForeignKey(City, related_name="users", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        
    def __str__(self):
        return f"{self.user}'s profile"
    
