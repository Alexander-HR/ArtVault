from django import forms
from accounts.models import Address
from finalization.models import Payment, Finalization

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street_name", "city", "postal_code", "country"]

class FinalizationForm(forms.ModelForm):
    class Meta:
        model = Finalization
        fields = ["national_id"]

    def clean_national_id(self):
        national_id = self.cleaned_data["national_id"]

        if len(national_id) != 10:
            raise forms.ValidationError("National ID must be 10 digits.")

        if not national_id.isdigit():
            raise forms.ValidationError("National ID must contain only digits.")

        return national_id

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["payment_type", "cardholder", "card_number", "card_expiration", "card_cvc", "bank_account", "bank_name", "routing_number", "account_number"]

    def clean(self):
        cleaned_data = super().clean()

        payment_type = cleaned_data.get("payment_type")
        if payment_type == "credit_card":
            for field in ["cardholder", "card_num", "card_expiry", "cvc"]:
                if not cleaned_data.get(field):
                    self.add_error(field,"This field is required.")
        elif payment_type == "bank_transfer":
            if not cleaned_data.get("bank_account"):
                self.add_error("bank_account", "This field is required.")
        elif payment_type == "wire_transfer":
            for field in ["bank_name", "routing_num", "account_num"]:
                if not cleaned_data.get(field):
                    self.add_error(field, "This field is required.")
        return cleaned_data

