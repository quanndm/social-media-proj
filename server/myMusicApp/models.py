from django.db import models
from django.contrib.auth.models import User

from django.core.validators import FileExtensionValidator
# Create your models here.

class Album(models.Model):  
    title = models.CharField(max_length=255 , blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    user_create = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    image_album = models.ImageField(upload_to="album", blank=True, null=True)
    def __str__(self):
        return self.title
class Song(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    artist = models.CharField(max_length=255, blank=True, null=True)
    file_url = models.FileField(upload_to="music", max_length=255, blank=True, null=True, validators=[FileExtensionValidator( ['mp3'] ) ])
    create_at = models.DateTimeField(auto_now_add=True)
    user_create = models.ForeignKey(User, blank=True, null=True, on_delete = models.CASCADE)
    album = models.ForeignKey(Album, related_name='songs',blank=True, null=True, on_delete= models.CASCADE)
    image_song = models.ImageField(upload_to="music", null=True, blank=True)
    def __str__(self):
        return self.title


