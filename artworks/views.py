from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from accounts.models import Seller
from bids.forms import BidForm
from bids.models import Bid
from .forms import ArtworkForm
from .models import Artwork, ArtworkImage, Favorite
from django.db.models import Max, Q


def artwork_detail(request, artwork_id):
    artwork = get_object_or_404(
        Artwork.objects.prefetch_related("images", "bids").annotate(
            highest_bid=Max('bids__amount', filter=~Q(bids__status='rejected'))
        ),
        id=artwork_id,
    )

    user_bid = None
    is_favorited = False

    if request.user.is_authenticated:
        user_bid = (
            Bid.objects.filter(artwork=artwork, buyer=request.user)
            .order_by("-created_at")
            .first()
        )

        is_favorited = Favorite.objects.filter(
            user=request.user, artwork=artwork
        ).exists()

    context = {
        "artwork": artwork,
        "images": artwork.images.all(),
        "user_bid": user_bid,
        "seller": getattr(artwork, "seller", None),
        "form": BidForm(artwork=artwork),
        "is_favorited": is_favorited
    }

    return render(request, "artworks/detail.html", context)


def index(request):
    artworks = Artwork.objects.prefetch_related("images").annotate(
        highest_bid=Max('bids__amount', filter=~Q(bids__status='rejected'))
    )

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

    favorited_ids = set()
    if request.user.is_authenticated:
        favorited_ids = set(
            Favorite.objects.filter(user=request.user).values_list('artwork_id', flat=True)
        )

    return render(request, "artworks/index.html", {
        "artworks": artworks,
        "medium_choices": Artwork.MEDIUM_CHOICES,
        "style_choices": Artwork.STYLE_CHOICES,
        "selected_medium": medium,
        "selected_style": style,
        "search": search,
        "order_by": order_by,
        "selected_sold": sold,
        "favorited_ids": favorited_ids,
    })


@login_required
def create_artwork(request):
    try:
        seller = request.user.seller
    except Seller.DoesNotExist:
        messages.error(request, "You must create a seller profile first.")
        return redirect("profile")

    if request.method == "POST":
        form = ArtworkForm(request.POST)

        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.seller = seller
            artwork.save()

            images = request.FILES.getlist("images")

            try:
                for image in images:
                    ArtworkImage.objects.create(
                        artwork=artwork,
                        image=image
                    )

                messages.success(request, "Artwork listed successfully.")
                return redirect("artworks:index")

            except Exception:
                messages.error(
                    request,
                    "Image upload failed. Please try again."
                )

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = ArtworkForm()

    return render(request, "artworks/create_artwork.html", {
        "form": form
    })

@login_required
def favorites(request):
    favorite_artworks = Artwork.objects.filter(favorited_by__user=request.user).prefetch_related("images")

    return render(request, "artworks/favorites.html", {
        "artworks": favorite_artworks
        })

@login_required
def toggle_favorite(request, artwork_id):
    if request.method != "POST":
        return redirect("artworks:artwork_detail", artwork_id=artwork_id)
    
    artwork = get_object_or_404(Artwork, id=artwork_id)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        artwork=artwork,
    )

    if not created:
        favorite.delete()
        messages.success(request, "Artwork removed from favorites")

    
    if created:
        messages.success(request, "Artwork added to favorites")

    return redirect("artworks:artwork_detail", artwork_id=artwork_id)