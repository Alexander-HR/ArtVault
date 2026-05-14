from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),

    path(
        'login',
        LoginView.as_view(template_name='accounts/login.html'),
        name='login'
    ),

    path('logout', LogoutView.as_view(), name='logout'),

    path("profile/", views.profile_view, name="profile"),

    path(
        "create-seller-profile/",
        views.create_seller_profile,
        name="create_seller_profile"
    ),

    path("sellers/", views.seller_list, name="sellers"),

    path(
        "sellers/<int:seller_id>/",
        views.seller_profile,
        name="seller_profile"
    ),

    path(
        "seller/artworks/",
        views.seller_listed_artworks,
        name="seller_listed_artworks"
    ),

    path(
        "notifications/",
        views.notifications_view,
        name="notifications"
    ),

    path("inbox/", views.inbox, name="inbox"),

    path(
        "message/<int:user_id>/",
        views.send_message,
        name="send_message"
    ),

    path(
        "message/<int:message_id>/read",
        views.message_read,
        name="message_read"
    ),
]