from django.shortcuts import render


def artwork_detail(request, artwork_id):
    artwork = {
        "id": artwork_id,
        "title": "Sample Artwork",
        "artist": "Sample Seller",
        "description": "This is a placeholder artwork detail page. Real artwork data will be connected later.",
        "starting_price": "1000 ISK",
        "status": "Available",
    }

    return render(request, "artworks/detail.html", {"artwork": artwork})
