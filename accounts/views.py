from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from artworks.models import Artwork
from .forms import ProfileForm
from .models import Profile, Seller

# Create your views here.


def register(request):
    if request.method == "POST":
        print(1)
    else:
        return render(request, "user/register.html", {
            "form": UserCreationForm()
        })

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")

        messages.error(request, "Profile update failed. Please check the errors below.")
    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, "profile.html", {
        "form": form,
        "profile": profile,
    })

def seller_profile(request, seller_id):
    seller = get_object_or_404(
        Seller.objects.select_related("user", "address"),
        id=seller_id,
    )

    artworks = (
        Artwork.objects
        .filter(seller=seller)
        .prefetch_related("images")
        .order_by("title")
    )

    return render(request, "accounts/seller_profile.html", {
        "seller": seller,
        "artworks": artworks,
    })
