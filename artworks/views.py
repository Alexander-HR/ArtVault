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
