from django.urls import path, include


urlpatterns = [
    path('auth/', include("myAuth.urls")),
    path('blogs/', include("myBlog.urls")),
    path('sounds/', include("myMusicApp.urls")),
]