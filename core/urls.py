from django.urls import path, include


urlpatterns = [
    path('auth/', include("myAuth.urls")),
    path('blog/', include("myBlog.urls")),
    path('sound/', include("myMusicApp.urls")),
]