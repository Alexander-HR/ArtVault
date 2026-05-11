from django.urls import path
from . import views

urlpatterns = [
    path("<int:artwork_id>/submit/", views.submit_bid, name="submit_bid"),
]