from django.urls import path
from . import views

app_name = "artworks"

urlpatterns = [
    path("new/", views.create_artwork, name="create_artwork"),
    path("<int:artwork_id>/", views.artwork_detail, name="artwork_detail"),
    path("", views.index, name="index"),
    path("favorites/", views.favorites, name="favorites"),
    path("<int:artwork_id>/favorite/", views.toggle_favorite, name="toggle_favorite"),
]