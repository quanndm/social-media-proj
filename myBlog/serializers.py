from rest_framework import serializers
from .models import Post, PostComment,PostLike
# code here

class PostSerializer(serializers.Serializer):
    class Meta:
        model = Post
        fields = "__all__"