from django.urls import path
from . import views

app_name = "bids"

urlpatterns = [
    path("<int:artwork_id>/submit/", views.submit_bid, name="submit_bid"),
    path("my-bids/", views.my_bids, name="my_bids"),

]