from datetime import date
import time
from .serializers import SongSerializer, AlbumSerializer
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Song, Album
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser,FormParser
from myMusicApp.Utility.functionHelpers import validateSong, validateAlbum
from rest_framework.decorators import action
from django.http import FileResponse
# Create your views here.
 
class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser,FormParser)
    def list(self, request):
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def retrieve(self, request, pk=None):
        try:
            song = Song.objects.get(pk=pk)
            serializer = SongSerializer(song)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Song.DoesNotExist:
            return Response({"msg":"Song not found!"},status=status.HTTP_404_NOT_FOUND)
    def create(self, request):
        if not request.user.is_authenticated:
            return Response({"msg":"User is not authenticated!"},status=status.HTTP_401_UNAUTHORIZED)
        try:
            data = request.POST
            obj = {
                "title": data.get("title", False) if "title" in data else None,
                "artist": data.get("artist", False) if "artist" in data else None,
                "file_url": request.FILES.get("file", False) if "file" in request.FILES else None,
                "user": request.user.pk
            }
            
            validate = validateSong(data=obj)
            if not validate[0]:
                return Response({"msg":validate[1]}, status=status.HTTP_400_BAD_REQUEST)
            obj["file_url"].name = "song_"+ str(obj["user"])+"_"+ date.today().strftime("%d%m%y")+"_" +str(round(time.time() * 1000))+ "." + obj["file_url"].name.split(".")[1].lower()
            song = Song.objects.create(title=obj["title"], artist=obj["artist"],user_create=User.objects.get(pk=obj["user"]), file_url=obj["file_url"])
            song.save()
            return Response({"msg":"Success!"},status=status.HTTP_201_CREATED)
        except:
            return Response({"msg":"Error creating song!"},status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({"msg":"User is not authenticated!"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            if pk is None:
                return Response({"msg":"Invalid pk!"},status=status.HTTP_400_BAD_REQUEST)
            song = Song.objects.get(pk=pk)
            # if song.user_create.pk != request.user.pk:
            #     return Response({"msg":"Only owner can update song!"},status=status.HTTP_401_UNAUTHORIZED)
            data = request.data
            obj = {
                "title": data.get("title", False) if "title" in data else None,
                "artist": data.get("artist", False) if "artist" in data else None,
                "file_url": request.FILES.get("file", False) if "file" in request.FILES else None,
                "user": request.user.pk
            }
            print(obj)

            return Response({"msg":"Update song!"},status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({"msg":"User is not authenticated!"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                song = Song.objects.get(pk=pk)
                song.file_url.delete()
                song.delete()
                return Response({"msg":"Delete song!"},status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({"msg":"Song not found!"},status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=True, permission_classes=(AllowAny,))
    def stream(self, request, pk=None):
        try:
            song = Song.objects.get(pk=pk)
            # get an open file handle (I'm just using a file attached to the model for this example):
            file_handle = song.file_url.open()
            #send file
            response = FileResponse(file_handle)
            response["Content-Type"] = "audio"
            response["Content-Length"] = song.file_url.size
            response["Content-Disposition"] = 'attachment; filename=%s' % (song.title.replace(" ","_")+"."+(song.file_url.name).split('.')[1])
            response["Name_song"] = song.title
            return response
        except:
            return Response({"msg":"Song not found!"},status=status.HTTP_404_NOT_FOUND)
        
class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser,FormParser)

    def list(self, request):
        album = Album.objects.all()
        # for al in album:
        #     songs = al.songs.all()
        #     print(songs)
        serializer = AlbumSerializer(album, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def retrieve(self, request, pk=None):
        try:
            album = Album.objects.get(pk=pk)
            
            serializer = AlbumSerializer(album)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"msg":"Album not found!"},status=status.HTTP_404_NOT_FOUND)
    def create(self, request):
        if not request.user.is_authenticated:
            return Response({"msg":"User is not authenticated!"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                data = request.POST
                obj = {
                    "title": data.get("title", False) if "title" in data else None,
                    "user_create": request.user.pk,
                    "image_album": request.FILES.get("image_album", False) if "image_album" in request.FILES else None,
                }
                validate = validateAlbum(obj)
                if not validate[0]:
                    return Response({"msg":validate[1]},status=status.HTTP_400_BAD_REQUEST)
                obj["image_album"].name = "Album_"+ str(obj["user_create"])+"_"+ date.today().strftime("%d%m%y")+"_" +str(round(time.time() * 1000))+ "." + obj["image_album"].name.split(".")[1].lower()
                album = Album.objects.create(title=obj["title"], user_create=User.objects.get(pk=obj["user_create"]), image_album=obj["image_album"])
                album.save()
                return Response({"msg":"Album created!"},status=status.HTTP_201_CREATED)
            except:
                return Response({"msg":"Invalid data!"},status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({"msg":"User is not authenticated!"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                #TODO: implement update method
                data = request.POST
                print(data)
                return Response({"msg":"Update success!"},status=status.HTTP_200_OK)
            except:
                return Response({"msg":"Update fail!"},status=status.HTTP_400_BAD_REQUEST)
    def partial_update(self, request, pk=None):
        return Response({"msg":"Method does not allowed!"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #TODO: check/test destroy method
    def destroy(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({"msg":"User is not authenticated!"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                try:
                    album = Album.objects.get(pk=pk)
                except Album.DoesNotExist:
                    return Response({"msg":"Album not found!"},status=status.HTTP_404_NOT_FOUND)
                
                # reset album of songs to null
                for song in album.songs.all():
                    song.album = None
                    song.save(update_fields=["album"])
                
                # delete album 
                album.delete()
                return Response({"msg":"Album deleted!"},status=status.HTTP_200_OK)
            except:
                return Response({"msg":"Delete Fail!"},status=status.HTTP_400_BAD_REQUEST)
