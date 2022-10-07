import uuid
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,related_name="user",on_delete=models.CASCADE, null=True, blank=True)
    DOB = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True,null=True)
    description = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True, default="M")
    avatar = models.ImageField(upload_to="profile_images", blank=True, null=True)

    def __str__(self):
        return self.user.username