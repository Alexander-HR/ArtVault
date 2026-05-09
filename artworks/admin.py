from django.contrib import admin
import artworks.models
# Register your models here.
admin.site.register(artworks.models.Artwork)
admin.site.register(artworks.models.ArtworkImage)