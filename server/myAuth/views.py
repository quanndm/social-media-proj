from datetime import datetime
import os
from django.shortcuts import render
from .serializers import (
    ChangePasswordSerializer,
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    UserProfileSerializer,
)

# ,UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile
from myAuth.utility.validateUpdateProfile import validateUpdateProfile
from myAuth.utility.validateEmail import isValidEmail
#from .permissions import userPermissions
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.parsers import MultiPartParser,FormParser
from django.conf import settings
from datetime import date
from django.core.files.storage import default_storage
from myApp.Utility import sendmail_forgot_pwd

# Create your views here.
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = UserSerializer

#     def list(self, request):
#         return Response(self.serializer_class(self.queryset, many=True).data,status=status.HTTP_200_OK)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     if self.action == 'list':
    #         permission_classes = [IsAuthenticated]
    #     else:
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]
    def list(self, request):
        if request.user.username not in  ["superadmin", "admin", "superuser"]:
            return Response({"msg": "You don't have permission to access this action"}, status=status.HTTP_403_FORBIDDEN)
        return Response(
            self.serializer_class(self.queryset, many=True).data,
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, pk=None):
        if pk is not None:
            try:
                self.queryset = Profile.objects.get(user=pk)
                return Response(
                    self.serializer_class(self.queryset).data, status=status.HTTP_200_OK
                )
            except:
                return Response({"msg": "Nothing"})
        return Response({"msg": "Nothing"})

    # method : PUT
    def update(self, request, pk=None):
        if pk is not None:
            try:
                obj = {
                    "user_name": request.data["user_name"],
                    "last_name": request.data["last_name"],
                    "first_name": request.data["first_name"],
                    "email": request.data["email"],
                    "DOB": request.data["DOB"],
                    "address": request.data["address"],
                    "description": request.data["description"],
                    "gender": request.data["gender"],
                }
                validate = validateUpdateProfile(obj, pk)
                
                if not validate[0]:
                    return Response({"msg": validate[1]}, status=status.HTTP_400_BAD_REQUEST)
                # cach 1


                # User.objects.filter(pk=pk).update(username=obj["user_name"],last_name=obj["last_name"],first_name=obj["first_name"],email=obj["email"])

                # Profile.objects.filter(user=pk).update(DOB=(datetime.strptime(obj["DOB"], '%d-%m-%Y').date() if obj["DOB"] else ""),address=obj["address"],description=obj["description"],gender=obj["gender"])
                
                # cach 2
                user = User.objects.get(pk=pk)
                user.username = obj["user_name"]
                user.last_name = obj["last_name"]
                user.first_name = obj["first_name"]
                user.email = obj["email"]
                user.save(update_fields=['username', 'first_name', 'last_name', 'email'])

                profile = Profile.objects.get(user=pk)
                profile.DOB = datetime.strptime(obj["DOB"], '%d-%m-%Y')
                profile.address = obj["address"]
                profile.gender = obj["gender"]
                profile.description = obj["description"]
                profile.save(update_fields=['DOB', 'gender', 'address', 'description'])



                return Response({"msg":"success"}, status=status.HTTP_200_OK)
            except:
                return Response({"msg": "Update fail!"}, status=status.HTTP_400_BAD_REQUEST)
            
    # method: PATCH
    def partial_update(self, request, pk=None):
        return Response({"msg": "API does not support method: PATCH"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@parser_classes([MultiPartParser, FormParser])
def uploadAvatar(request, pk=None):
    if request.method == 'POST':
        user = User.objects.get(pk=pk)
        if user is None:
            return Response({"message":"User not found!"}, status=status.HTTP_400_BAD_REQUEST)
       
        if request.user.username != user.username:
            return Response({"message": "Cannot upload avatar for another user."}, status=status.HTTP_400_BAD_REQUEST)
        data  = request.data["file"]
        try:
            profile = Profile.objects.get(user = user)
            profile.avatar.delete()
            data.name = "avatar_" +str(user.pk) + "_" + date.today().strftime("%d%m%y") + "." + data.name.split(".")[1].lower()
            profile.avatar = data
            profile.save(update_fields=["avatar"])
            return Response({"message": "Uploaded avatar success."}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Uploaded avatar fail."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])            
def forgotPwd(request):
    if request.method == 'POST':
        email = request.data.get("email")
        if email is None:
            return Response({"message": "Email can not be null"}, status=status.HTTP_400_BAD_REQUEST)
        if not isValidEmail(email):
            return Response({"message": "Email is invalid"}, status=status.HTTP_400_BAD_REQUEST)
        # send mail to user to reset password
        # sendmail_forgot_pwd(email)
        
        return Response({"message": "If you have registered, you can receive an email to reset password"}, status=status.HTTP_200_OK)
        