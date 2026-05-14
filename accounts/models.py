from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username


class Address(models.Model):
    COUNTRY_CHOICES = [
        ("Iceland", "Iceland"),
        ("Denmark", "Denmark"),
        ("Norway", "Norway"),
        ("Sweden", "Sweden"),
        ("United Kingdom", "United Kingdom"),
        ("United States", "United States"),
    ]

    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    country = models.CharField(
        max_length=20,
        choices=COUNTRY_CHOICES,
        default="Iceland"
    )


class Seller(models.Model):
    SELLER_TYPE_CHOICES = [
        ("individual", "Individual"),
        ("gallery", "Gallery"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    type = models.CharField(
        max_length=20,
        choices=SELLER_TYPE_CHOICES,
        default="individual"
    )

    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    logo = models.ImageField(
        upload_to="seller_images/logos",
        blank=True,
        null=True
    )

    cover_image = models.ImageField(
        upload_to="seller_images/covers",
        blank=True,
        null=True
    )

    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    artwork = models.ForeignKey(
        "artworks.Artwork",
        on_delete=models.CASCADE
    )

    bid = models.ForeignKey(
        "bids.Bid",
        on_delete=models.CASCADE
    )

    message = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    subject = models.CharField(max_length=100)

    body = models.TextField()

    read = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver}'