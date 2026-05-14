from django import forms
from .models import Address, Profile, Seller, User, Message
from django.contrib.auth.forms import UserCreationForm

class ProfileForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Profile
        fields = ["image"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "form-control"})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["name"].initial = self.user.first_name or self.user.username

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Name cannot be empty.")
        return name

    def save(self, commit=True):
        profile = super().save(commit=False)
        self.user.first_name = self.cleaned_data["name"]

        if commit:
            self.user.save()
            profile.save()

        return profile
    
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = UserCreationForm.Meta.fields

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street_name", "city", "postal_code", "country"]
        widgets = {
            "street_name": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.Select(attrs={"class": "form-control"}),
        }


class SellerProfileForm(forms.ModelForm):
    logo = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )
    cover_image = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Seller
        fields = ["type", "bio", "logo", "cover_image"]
        widgets = {
            "type": forms.Select(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]