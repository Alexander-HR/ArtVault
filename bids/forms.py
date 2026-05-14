from django import forms
from .models import Bid

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount", 
                  "expires_at"]
        widgets = {
            "expires_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        self.artwork = kwargs.pop("artwork", None)
        super().__init__(*args, **kwargs)
    
    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if self.artwork:
            from bids.models import Bid
            highest = (
                Bid.objects
                .filter(artwork=self.artwork)
                .exclude(status="rejected")
                .order_by("-amount")
                .values_list("amount", flat=True)
                .first()
            )
            floor = highest if highest is not None else self.artwork.starting_bid
            if amount <= floor:
                raise forms.ValidationError(
                    f"Your bid must be higher than {floor} ISK."
                )
        return amount
    def clean_expires_at(self):
        expires_at = self.cleaned_data["expires_at"]

        from django.utils import timezone

        if expires_at <= timezone.now():
            raise forms.ValidationError(
                "Expiration date must be in the future."
            )

        return expires_at
