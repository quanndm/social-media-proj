from rest_framework import serializers
from .models import Song, Album

class SongSerializer(serializers.ModelSerializer):
    url_stream = serializers.SerializerMethodField('get_url_stream')
    class Meta:
        model = Song
        fields = ("pk","title","artist","file_url","create_at","user_create","album","url_stream")
    def get_url_stream(self, song):
      return f"/api/sound/song/{song.pk}/stream/"
class AlbumSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True)
    class Meta:
        model = Album
        fields = ("pk","title","songs","image_album","create_at","user_create")

