from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm, CustomUserCreationForm
from .models import Profile


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})

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
    seller = {
        "id": seller_id,
        "username": "Sample Seller",
        "bio": "This is a placeholder seller profile. Real seller information will be connected later.",
        "location": "Reykjavik, Iceland",
        "member_since": "2026",
    }

    artworks = [
        {"title": "Sample Artwork 1", "status": "Available", "price": "1000 ISK"},
        {"title": "Sample Artwork 2", "status": "Available", "price": "2500 ISK"},
        {"title": "Sample Artwork 3", "status": "Sold", "price": "4000 ISK"},
    ]

    return render(request, "accounts/seller_profile.html", {
        "seller": seller,
        "artworks": artworks,
    })
    return render(
        request,
        "accounts/seller_profile.html",
        {
            "seller": seller,
            "artworks": artworks,
        },
    )
