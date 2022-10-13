from rest_framework import serializers
from .models import Song, Album

class SongSerializer(serializers.ModelSerializer):
    album_id = serializers.StringRelatedField(source="album.pk")
    class Meta:
        model = Song
        fields = ("pk","title","artist","file_url","create_at","user_create","album_id")

class AlbumSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True)
    class Meta:
        model = Album
        fields = ("pk","title","songs","create_at","user_create")
