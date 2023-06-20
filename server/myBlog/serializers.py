from rest_framework import serializers
from .models import Post, PostComment,PostLike
# code here 

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id","user","content","image_url","like_count","create_at")