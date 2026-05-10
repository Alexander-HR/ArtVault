from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ProfileForm
from .models import Profile, Seller

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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

def seller_list(request):
    sellers = Seller.objects.all()

    return render(request, "accounts/seller_list.html", {
        "sellers": sellers,
    })
    return render(
        request,
        "accounts/seller_profile.html",
        {
            "seller": seller,
            "artworks": artworks,
        },
    )
