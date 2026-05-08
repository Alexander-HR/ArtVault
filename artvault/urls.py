from django.contrib import admin
from django.urls import path, include
from django.urls import path, include

import artworks
from artvault import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path("artworks/", include("artworks.urls")),
]
