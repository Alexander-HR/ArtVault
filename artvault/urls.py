from django.contrib import admin
from django.urls import path, include
from artvault import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # ✅ profile + accounts
    path('', include('accounts.urls')),
    path("artworks/", include("artworks.urls")),
]