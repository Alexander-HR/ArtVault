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

    return render(request, "artworks/detail.html", context)


def index(request):
    artworks = Artwork.objects.all()
    return render(request, "artworks/index.html", {"artworks": artworks})
