from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile_view(request):
    return render(request, "profile.html")

def seller_profile(request, seller_id):
    seller = {
        "id": seller_id,
        "username": "Sample Seller",
        "bio": "This is a placeholder seller profile. Real seller information will be connected later.",
        "location": "Reykjavik, Iceland",
        "member_since": "2026",
    }

    artworks = [
        {
            "title": "Sample Artwork 1",
            "status": "Available",
            "price": "1000 ISK",
        },
        {
            "title": "Sample Artwork 2",
            "status": "Available",
            "price": "2500 ISK",
        },
        {
            "title": "Sample Artwork 3",
            "status": "Sold",
            "price": "4000 ISK",
        },
    ]

    return render(
        request,
        "accounts/seller_profile.html",
        {
            "seller": seller,
            "artworks": artworks,
        },
    )