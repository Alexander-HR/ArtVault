from django.urls import path
from . import views

app_name = "artworks"

urlpatterns = [
    path("<int:artwork_id>/", views.artwork_detail, name="artwork_detail"),
]