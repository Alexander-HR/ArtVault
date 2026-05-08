from django.shortcuts import render
from artworks.models import Artwork

def artwork_detail(request, artwork_id):
    artwork = {
        "id": artwork_id,
        "title": "Sample Artwork",
        "artist": "Sample Seller",
        "description": "This is a placeholder artwork detail page. Real artwork data will be connected later.",
        "starting_price": "1000 ISK",
        "status": "Available",
    }

    return render(request, "artworks/detail.html", {"artwork": artwork})


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
