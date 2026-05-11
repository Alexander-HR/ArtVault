from django.urls import path
from . import views

urlpatterns = [
    path("<int:artwork_id>/submit/", views.submit_bid, name="submit_bid"),
    path("seller/overview/", views.seller_bids_overview, name="seller_bids_overview"),
    path("<int:bid_id>/accept/", views.accept_bid, name="accept_bid"),
]