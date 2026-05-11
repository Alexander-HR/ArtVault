from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from artworks.models import Artwork
from .forms import BidForm

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
        messages.success(request, "Bid submitted successfully.")
    else:
        messages.error(request, "Invalid bid. Please check the amount.")

    return redirect("artworks:artwork_detail", artwork_id=artwork_id)

@login_required
def my_bids(request):
    bids = request.user.bids.select_related("artwork").order_by
    ("-created_at")
    return render(request, "my-bids.html", {"bids":bids})