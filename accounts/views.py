from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404, redirect, render
from artworks.models import Artwork
from .models import Profile, Seller
from .forms import AddressForm, CustomUserCreationForm, ProfileForm, SellerProfileForm
from .models import Notification

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

    has_seller_profile = Seller.objects.filter(user=request.user).exists()

    return render(request, "profile.html", {
        "form": form,
        "profile": profile,
        "has_seller_profile": has_seller_profile,
    })

@login_required
def create_seller_profile(request):
    if Seller.objects.filter(user=request.user).exists():
        messages.info(request, "You already have a seller profile.")
        return redirect("profile")

    if request.method == "POST":
        seller_form = SellerProfileForm(request.POST, request.FILES)
        address_form = AddressForm(request.POST)

        if seller_form.is_valid() and address_form.is_valid():
            address = address_form.save()

            logo_file = seller_form.cleaned_data["logo"]
            cover_image_file = seller_form.cleaned_data["cover_image"]

            logo_path = default_storage.save(
                f"seller_images/logos/{logo_file.name}",
                logo_file
            )
            cover_image_path = default_storage.save(
                f"seller_images/covers/{cover_image_file.name}",
                cover_image_file
            )

            seller = seller_form.save(commit=False)
            seller.user = request.user
            seller.address = address
            seller.logo = default_storage.url(logo_path)
            seller.cover_image = default_storage.url(cover_image_path)
            seller.save()

            messages.success(request, "Seller profile created successfully.")
            return redirect("profile")

        messages.error(request, "Seller profile creation failed. Please check the errors below.")
    else:
        seller_form = SellerProfileForm()
        address_form = AddressForm()

    return render(request, "accounts/create_seller_profile.html", {
        "seller_form": seller_form,
        "address_form": address_form,
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


def seller_list(request):
    sellers = Seller.objects.all()

    return render(request, "accounts/seller_list.html", {
        "sellers": sellers,
    })

@login_required
def notifications_view(request):
    notifications = (
        Notification.objects
        .filter(recipient=request.user)
        .select_related("artwork", "bid")
        .order_by("-created_at")
    )

    notifications.update(is_read=True)

    return render(request, "accounts/notifications.html", {
        "notifications": notifications,
    })