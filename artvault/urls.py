from django.contrib import admin
from django.urls import path, include
from django.urls import path, include

import artworks
from artvault import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("", include("accounts.urls")),
    path("artworks/", include("artworks.urls")),
    path("bids/", include("bids.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
