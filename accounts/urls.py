from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import profile_view, seller_profile, seller_list, seller_listed_artworks
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path("profile/", profile_view, name="profile"),
    path("sellers/", views.seller_list, name="sellers"),
    path("sellers/<int:seller_id>/", seller_profile, name="seller_profile"),
    path("seller/artworks/", seller_listed_artworks, name="seller_listed_artworks"),
]
