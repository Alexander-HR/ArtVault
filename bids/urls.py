from django.urls import path
from . import views

app_name = "bids"

urlpatterns = [
    path("<int:artwork_id>/submit/", views.submit_bid, name="submit_bid"),
    path("my-bids/", views.my_bids, name="my_bids"),

    path("seller-dashboard/", views.seller_dashboard, name="seller_dashboard"),

    path("seller/overview/", views.seller_bids_overview, name="seller_bids_overview"),
    path("<int:bid_id>/accept/", views.accept_bid, name="accept_bid"),
    path("<int:bid_id>/resubmit/", views.resubmit_bid, name="resubmit_bid"),
]