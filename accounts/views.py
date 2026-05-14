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