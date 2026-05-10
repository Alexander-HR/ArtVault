from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_images/", blank=True, null=True)

    def __str__(self):
        return self.user.username

class Address(models.Model):
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

class Seller(models.Model):
    SELLER_TYPE_CHOICES = [
        ("individual", "Individual"),
        ("gallery", "Gallery"),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=SELLER_TYPE_CHOICES, default="individual")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    logo = models.CharField(max_length=255)
    cover_image = models.CharField(max_length=255)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username