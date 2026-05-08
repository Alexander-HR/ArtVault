from django.conf import settings
from django.db import models

from artworks.models import Artwork
from accounts.models import User

class Bid(models.Model):
    STATUS_CHOICES = (
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('contingent', 'Contingent'),
    ('pending', 'Pending'),
    ('finalized', 'Finalized'),
    )
    id = models.AutoField(primary_key=True)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='bids')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return str(self.id)
