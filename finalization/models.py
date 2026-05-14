from django.db import models

from bids.models import Bid
from accounts.models import Address

class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('wire_transfer', 'Wire Transfer'),]
    payment_type = models.CharField(max_length=30, choices=PAYMENT_CHOICES)

    cardholder = models.CharField(max_length=30, blank=True)
    card_number = models.CharField(max_length=30, blank=True)
    card_expiration = models.CharField(max_length=30, blank=True)
    card_cvc = models.CharField(max_length=30, blank=True)

    bank_account = models.CharField(max_length=30, blank=True)

    bank_name = models.CharField(max_length=30, blank=True)
    routing_number = models.CharField(max_length=30, blank=True)
    account_number = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.get_payment_type_display()

class Finalization(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='finalization', null=True, blank=True)
    bid = models.ForeignKey("bids.Bid", on_delete=models.CASCADE, related_name='finalization')
    address = models.ForeignKey("accounts.Address", on_delete=models.CASCADE, related_name='finalization', null=True, blank=True)
    national_id = models.CharField(max_length=30, blank=True)
    date_finalized = models.DateField(null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    def __str__(self):
        return f'Finalization for bid {self.bid}'