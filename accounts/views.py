<<<<<<< HEAD
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404, redirect, render

from artworks.models import Artwork

from .forms import (
    AddressForm,
    CustomUserCreationForm,
    ProfileForm,
    SellerProfileForm,
    MessageForm,
)

from .models import (
    Profile,
    Seller,
    User,
    Message,
    Notification,
)


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
def seller_listed_artworks(request):
    seller = Seller.objects.filter(user=request.user).first()

    artworks = []

    if seller:
        artworks = (
            Artwork.objects
            .filter(seller=seller)
            .prefetch_related("images", "bids")
            .order_by("title")
        )

    return render(request, "accounts/seller_listed_artworks.html", {
        "seller": seller,
        "artworks": artworks,
    })

@login_required
def create_seller_profile(request):

    if Seller.objects.filter(user=request.user).exists():
        messages.info(
            request,
            "You already have a seller profile."
        )

        return redirect("profile")

    if request.method == "POST":
        seller_form = SellerProfileForm(
            request.POST,
            request.FILES
        )

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

            seller.cover_image = default_storage.url(
                cover_image_path
            )

            seller.save()

            messages.success(
                request,
                "Seller profile created successfully."
            )

            return redirect("profile")

        messages.error(
            request,
            "Seller profile creation failed. Please check the errors below."
        )

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
=======
    artworks = []

    if seller:
        artworks = (
            Artwork.objects
            .filter(seller=seller)
            .prefetch_related("images", "bids")
            .order_by("title")
        )

    return render(request, "accounts/seller_listed_artworks.html", {
>>>>>>> 1cae0507d76a1f746c839346680ec7252ac99e04
        "seller": seller,
        "artworks": artworks,
    })


<<<<<<< HEAD
def seller_list(request):

    sellers = Seller.objects.all()

    return render(request, "accounts/seller_list.html", {
        "sellers": sellers,
    })


=======
>>>>>>> 1cae0507d76a1f746c839346680ec7252ac99e04
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


@login_required
def send_message(request, user_id):
<<<<<<< HEAD

=======
>>>>>>> 1cae0507d76a1f746c839346680ec7252ac99e04
    receiver = get_object_or_404(User, id=user_id)

    if request.method == "POST":

        form = MessageForm(request.POST)

        if form.is_valid():

            message = form.save(commit=False)

            message.receiver = receiver
            message.sender = request.user

            message.save()

            messages.success(request, "Message sent.")

            return redirect("inbox")

    else:
        form = MessageForm()

    return render(request, "accounts/send_message.html", {
        "form": form,
        "receiver": receiver,
    })


@login_required
def inbox(request):

    tab = request.GET.get("tab", "unread")

    received_messages = (
        Message.objects
        .filter(receiver=request.user)
        .order_by("-date_created")
    )

    if tab == "unread":
        received_messages = received_messages.filter(read=False)

    return render(request, "accounts/inbox.html", {
        "received_messages": received_messages,
        "tab": tab,
    })


@login_required
def message_read(request, message_id):
    message = get_object_or_404(
        Message,
        id=message_id,
        receiver=request.user
    )

    message.read = True
    message.save()

    next_url = request.GET.get("next")

    if next_url:
        return redirect(next_url)

    return redirect("inbox")