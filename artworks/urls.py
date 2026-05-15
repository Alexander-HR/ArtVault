from django.urls import path
from . import views

app_name = "artworks"

urlpatterns = [
    path("new/", views.create_artwork, name="create_artwork"),
    path("<int:artwork_id>/", views.artwork_detail, name="artwork_detail"),
    path("", views.index, name="index"),
]