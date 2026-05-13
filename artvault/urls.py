from django.contrib import admin
from artvault import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("", include("accounts.urls")),
    path("artworks/", include("artworks.urls")),
    path("finalize/", include("finalization.urls")),
    path("bids/", include("bids.urls")),

    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path("contact/", TemplateView.as_view(template_name="pages/contact.html"), name="contact"),
    path("help/", TemplateView.as_view(template_name="pages/help.html"), name="help"),
    path("privacy/", TemplateView.as_view(template_name="pages/privacy.html"), name="privacy"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
