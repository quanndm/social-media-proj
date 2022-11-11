from django.urls import path, include
from rest_framework import routers
from .views import SongViewSet, AlbumViewSet
# code here
router = routers.DefaultRouter()
router.register(r'song', SongViewSet)
router.register(r'album', AlbumViewSet)

urlpatterns = [
    path("", include(router.urls))
]