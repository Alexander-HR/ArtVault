from django.shortcuts import get_object_or_404, render

from .models import Artwork
from bids.models import Bid


def artwork_detail(request, artwork_id):
    artwork = get_object_or_404(
        Artwork.objects.prefetch_related("images", "bids"),
        id=artwork_id,
    )

    user_bid = None

    if request.user.is_authenticated:
        user_bid = (
            Bid.objects.filter(artwork=artwork, buyer=request.user)
            .order_by("-created_at")
            .first()
        )

    context = {
        "artwork": artwork,
        "images": artwork.images.all(),
        "user_bid": user_bid,
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
