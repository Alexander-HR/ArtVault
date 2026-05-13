from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone

from artworks.models import Artwork
from .forms import BidForm
from .models import Bid
from accounts.models import Seller


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
    tab = request.GET.get('tab', 'active')
    bids = request.user.bids.select_related("artwork").order_by("-created_at")

    if tab == 'active':
        bids = bids.filter(expires_at__gt=timezone.now())
    elif tab == 'accepted':
        bids = bids.filter(status__in=['accepted', 'contingent'])
    elif tab == 'pending':
        bids = bids.filter(status='pending')

    return render(request, "my-bids.html", {
        "bids": bids,
        "active_tab": tab
    })


@login_required
def seller_dashboard(request):

    seller = get_object_or_404(Seller, user=request.user)

    current_bids = Bid.objects.filter(
        artwork__seller=seller,
        artwork__sold=False
    ).select_related("artwork", "buyer")

    previous_sales = Bid.objects.filter(
        artwork__seller=seller,
        artwork__sold=True,
        status="finalized"
    ).select_related("artwork", "buyer")

    return render(request, "bids/seller_bids_overview.html", {
        "current_bids": current_bids,
        "previous_sales": previous_sales,
    })