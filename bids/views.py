from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import Seller, Notification
from artworks.models import Artwork
from .forms import BidForm
from .models import Bid


@login_required
def submit_bid(request, artwork_id):
    if request.method != "POST":
        return redirect("artworks:artwork_detail", artwork_id=artwork_id)

    artwork = get_object_or_404(Artwork, pk=artwork_id)
    form = BidForm(request.POST, artwork=artwork)

    if form.is_valid():
        bid = form.save(commit=False)
        bid.artwork = artwork
        bid.buyer = request.user
        bid.save()

        try:
            Notification.objects.create(
                recipient=artwork.seller.user,
                artwork=artwork,
                bid=bid,
                message=(
                    f"New bid on {artwork.title}: "
                    f"{bid.amount} ISK"
                )
            )
        except Exception:
            pass

        messages.success(request, "Bid submitted successfully.")
    else:
        messages.error(request, "Invalid bid. Please check the amount.")

    return redirect("artworks:artwork_detail", artwork_id=artwork_id)


@login_required
def my_bids(request):
    tab = request.GET.get("tab", "active")

    bids = (
        request.user.bids
        .select_related("artwork")
        .order_by("-created_at")
    )

    if tab == "active":
        bids = bids.filter(expires_at__gt=timezone.now())

    elif tab == "accepted":
        bids = bids.filter(status__in=["accepted", "contingent"])

    elif tab == "pending":
        bids = bids.filter(status="pending")

    return render(request, "my-bids.html", {
        "bids": bids,
        "active_tab": tab,
    })


@login_required
def seller_bids_overview(request):
    seller = Seller.objects.filter(user=request.user).first()

    if not seller:
        messages.error(request, "You need a seller profile to view bids.")
        return redirect("home")

    bids = (
        Bid.objects
        .filter(artwork__seller=seller)
        .select_related("artwork", "buyer")
        .order_by("-created_at")
    )

    return render(request, "bids/seller_bids_overview.html", {
        "bids": bids,
    })


@login_required
@transaction.atomic
def accept_bid(request, bid_id):

    if request.method != "POST":
        return redirect("bids:seller_bids_overview")

    seller = Seller.objects.filter(user=request.user).first()

    if not seller:
        messages.error(request, "You need a seller profile to accept bids.")
        return redirect("home")

    bid = get_object_or_404(
        Bid.objects.select_related("artwork", "buyer"),
        id=bid_id,
        artwork__seller=seller,
    )

    artwork = bid.artwork

    if artwork.sold:
        messages.error(request, "This artwork has already been sold.")
        return redirect("bids:seller_bids_overview")

    if bid.status != "pending":
        messages.error(request, "Only pending bids can be accepted.")
        return redirect("bids:seller_bids_overview")

    if bid.expires_at < timezone.now():
        messages.error(request, "This bid has expired and cannot be accepted.")
        return redirect("bids:seller_bids_overview")

    bid.status = "accepted"
    bid.save()

    artwork.sold = True
    artwork.save()

    try:
        Notification.objects.create(
            recipient=bid.buyer,
            artwork=artwork,
            bid=bid,
            message=(
                f"Your bid on {artwork.title} "
                f"was accepted."
            )
        )
    except Exception:
        pass

    messages.success(
        request,
        "Bid accepted successfully. The artwork is now marked as sold."
    )

    return redirect("bids:seller_bids_overview")