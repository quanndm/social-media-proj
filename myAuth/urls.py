from django.urls import path, include
from .views import ChangePasswordView, MyObtainTokenPairView,RegisterView,UserProfileViewSet, uploadAvatar
# ,UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
router.register(r'user_profiles',UserProfileViewSet) 
urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('change_avatar/<int:pk>/', uploadAvatar,name="change_avatar"),
    path("", include(router.urls)),
]  