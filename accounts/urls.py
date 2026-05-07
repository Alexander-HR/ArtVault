from django.urls import path
from .views import profile_view, seller_profile

urlpatterns = [
    path("profile/", profile_view, name="profile"),
    path("sellers/<int:seller_id>/", seller_profile, name="seller_profile"),
]