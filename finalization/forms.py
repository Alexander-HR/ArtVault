from django import forms
import re
from accounts.models import Address
from finalization.models import Payment, Finalization

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street_name", "city", "postal_code", "country"]

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get("postal_code")

        if not postal_code.isdigit():
            raise forms.ValidationError(
                "Postal code must contain only digits."
            )
        return postal_code

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

    def clean_cardholder(self):
        cardholder = self.cleaned_data.get("cardholder")

        if cardholder and not re.match(r"^[A-Za-zÀ-ÿ\s'-]+$", cardholder):
            raise forms.ValidationError("Cardholder name can only contain letters.")

        return cardholder

    def clean_card_num(self):
        card_num = self.cleaned_data.get("card_number")

        if card_num:
            card_num = card_num.replace(" ", "")

            if not card_num.isdigit():
                raise forms.ValidationError("Card number must contain only digits.")

            if len(card_num) != 16:
                raise forms.ValidationError("Card number must be 16 digits.")

        return card_num

    def clean_card_expiry(self):
        expiry = self.cleaned_data.get("card_expiration")

        if expiry and not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", expiry):
            raise forms.ValidationError("Expiry date must be in MM/YY format.")

        return expiry

    def clean_cvc(self):
        cvc = self.cleaned_data.get("card_cvc")

        if cvc:
            if not cvc.isdigit():
                raise forms.ValidationError("CVC must contain only numbers.")

            if len(cvc) != 3:
                raise forms.ValidationError("CVC must be 3 digits.")

        return cvc

    def clean_bank_account(self):
        bank_account = self.cleaned_data.get("bank_account")

        if bank_account:
            pattern = r"^\d{4}-\d{2}-\d{6}$"

            if not re.match(pattern, bank_account):
                raise forms.ValidationError("Bank account must be in format xxxx-xx-xxxxxx.")

        return bank_account

    def clean_bank_name(self):
        bank_name = self.cleaned_data.get("bank_name")

        if bank_name and not re.match(r"^[A-Za-zÀ-ÿ0-9\s&.'-]+$", bank_name):
            raise forms.ValidationError("Bank name contains invalid characters.")

        return bank_name

    def clean_routing_num(self):
        routing_num = self.cleaned_data.get("routing_number")

        if routing_num:
            routing_num = routing_num.replace(" ", "").replace("-", "")

            if not routing_num.isdigit():
                raise forms.ValidationError("Routing number can only contain numbers.")

            if len(routing_num) != 9:
                raise forms.ValidationError("Routing number must be 9 digits.")

        return routing_num

    def clean_account_num(self):
        account_num = self.cleaned_data.get("account_number")
        if account_num:
            account_num = account_num.replace(" ", "").replace("-", "")

            if not account_num.isdigit():
                raise forms.ValidationError("Account number must contain only digits.")

            if len(account_num) < 6 or len(account_num) > 17:
                raise forms.ValidationError("Account number must be between 6-17 digits.")

        return account_num

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

