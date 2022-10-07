from django.urls import path, include
from .views import demo, PostViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'post',PostViewSet)
urlpatterns = [
    path("demo", demo, name="demo"),
    path("", include(router.urls))
]
