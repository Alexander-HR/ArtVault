from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from bids.models import Bid
from accounts.models import Address
from finalization.models import Finalization, Payment
from finalization.forms import FinalizationForm, PaymentForm, AddressForm

@login_required
def contact_step(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)

    finalization, created = Finalization.objects.get_or_create(bid=bid)

    if request.method == "POST":
        address_form = AddressForm(request.POST)
        finalization_form = FinalizationForm(request.POST, instance=finalization)

        if address_form.is_valid() and finalization_form.is_valid():
            address = address_form.save()
            finalization = finalization_form.save(commit=False)
            finalization.address = address
            finalization.save()

            return redirect("finalization:review_step", bid_id=bid.id)

    else:
        if finalization.address:
            address_form = AddressForm(instance=finalization.address)
        else:
            address_form = AddressForm()
        finalization_form = FinalizationForm(instance = finalization)

    return render(request, "finalizations/contact_step.html", {
        "bid": bid,
        "address_form": address_form,
        "finalization_form": finalization_form,
    })


def payment_step(request):
    pass

@login_required
def review_step(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)
    finalization = get_object_or_404(Finalization, bid=bid)

    return render(request, "finalizations/review_step.html", {
        "bid": bid,
        "finalization": finalization,
    })

def confirmation_step(request):
    pass