from django.shortcuts import render, get_object_or_404
from artworks.models import Artwork


def artwork_detail(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    seller = getattr(artwork, "seller", None)

    return render(request, "artworks/detail.html", {
        "artwork": artwork,
        "seller": seller,
    })


def index(request):
    artworks = [
        {
            "id": 1,
            "title": "Sunset Over Reykjavik",
            "starting_bid": 500,
            "medium": "Oil painting",
            "dimensions": "50 x 70 cm",
            "sold": False,
            "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee"
        },
        {
            "id": 2,
            "title": "Abstract Waves",
            "starting_bid": 750,
            "medium": "Acrylic",
            "dimensions": "60 x 60 cm",
            "sold": True,
            "image": "https://helloart.com/cdn/shop/products/1_1699990399_30193.jpg?v=1700067461"
        }
    ]
    return render(request, 'artworks/index.html', {'artworks': artworks})