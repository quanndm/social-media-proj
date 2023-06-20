import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    image_url = models.ImageField(upload_to="blog", blank=True, null=True)
    like_count = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now=True)

class PostLike(models.Model):
    post = models.ForeignKey(Post, related_name="post_likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now=True)
class PostComment(models.Model):
    post = models.ForeignKey(Post,related_name="post_comments" , on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500, blank=True, null=True)
    create_at = models.DateTimeField(auto_now=True)

