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
    artworks = Artwork.objects.prefetch_related("images")

    search = request.GET.get("search")
    medium = request.GET.get("medium")
    style = request.GET.get("style")
    order_by = request.GET.get("order_by")
    sold = request.GET.get("sold")

    if search:
        artworks = artworks.filter(title__icontains=search)

    if medium:
        artworks = artworks.filter(medium=medium)

    if style:
        artworks = artworks.filter(style=style)

    if order_by in ["starting_bid", "-starting_bid", "title", "-title"]:
        artworks = artworks.order_by(order_by)

    if sold == "sold":
        artworks = artworks.filter(sold=True)

    elif sold == "available":
        artworks = artworks.filter(sold=False)

    return render(request, "artworks/index.html", {
        "artworks": artworks,
        "medium_choices": Artwork.MEDIUM_CHOICES,
        "style_choices": Artwork.STYLE_CHOICES,
        "selected_medium": medium,
        "selected_style": style,
        "search": search,
        "order_by": order_by,
        "selected_sold": sold,})
    artworks = Artwork.objects.all()

    search = request.GET.get("search")
    medium = request.GET.get("medium")
    style = request.GET.get("style")
    order_by = request.GET.get("order_by")
    sold = request.GET.get("sold")

    if search:
        artworks = artworks.filter(title__icontains=search)

    if medium:
        artworks = artworks.filter(medium=medium)

    if style:
        artworks = artworks.filter(style=style)

    if order_by in ["starting_bid", "-starting_bid", "title", "-title"]:
        artworks = artworks.order_by(order_by)

    if sold == "sold":
        artworks = artworks.filter(sold=True)

    elif sold == "available":
        artworks = artworks.filter(sold=False)

    return render(request, "artworks/index.html", {
        "artworks": artworks,
        "medium_choices": Artwork.MEDIUM_CHOICES,
        "style_choices": Artwork.STYLE_CHOICES,
        "selected_medium": medium,
        "selected_style": style,
        "search": search,
        "order_by": order_by,
        "selected_sold": sold,})

