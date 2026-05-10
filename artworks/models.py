from django.conf import settings
from django.db import models
from accounts.models import User

class Artwork(models.Model):
    MEDIUM_CHOICES = [
        ('oil', 'Oil painting'),
        ('water', 'Watercolour Painting'),
        ('sculpture', 'Sculpture'),
        ('photo', 'Photography'),
        ('other', 'Other')
    ]
    STYLE_CHOICES = [
        ('abstract', 'Abstract'),
        ('realism', 'Realism'),
        ('impressionism', 'Impressionism'),
        ('modern', 'Modern'),
        ('other', 'Other')
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    medium = models.CharField(choices=MEDIUM_CHOICES, max_length=50)
    style = models.CharField(choices=STYLE_CHOICES, max_length=50)
    starting_bid = models.PositiveIntegerField(default=0)
    date_listed = models.DateField(auto_now=False, auto_now_add=True)
    sold = models.BooleanField(default=False)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dimensions = models.CharField(max_length=50)
    year_created = models.PositiveIntegerField()
    edition = models.CharField(max_length=50)
    provenance = models.TextField()
    def __str__(self):
        return f'{self.title}, {self.id}'

class ArtworkImage(models.Model):
    id = models.AutoField(primary_key=True)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='images')
    image_path = models.CharField(max_length=255)
    def __str__(self):
        return f'Image for {self.artwork.title}'
