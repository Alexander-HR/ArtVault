from django import forms
from .models import Artwork


class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = [
            "title",
            "medium",
            "style",
            "starting_bid",
            "dimensions",
            "year_created",
            "edition",
            "provenance",
            "artist_name",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "medium": forms.Select(attrs={"class": "form-control"}),
            "style": forms.Select(attrs={"class": "form-control"}),
            "starting_bid": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "dimensions": forms.TextInput(attrs={"class": "form-control"}),
            "year_created": forms.NumberInput(attrs={"class": "form-control"}),
            "edition": forms.TextInput(attrs={"class": "form-control"}),
            "provenance": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "artist_name": forms.TextInput(attrs={"class": "form-control"}),
        }