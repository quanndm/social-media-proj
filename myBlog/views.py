from datetime import date
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from rest_framework import viewsets,status
from .models import Post
from .serializers import PostSerializer 
from rest_framework.parsers import MultiPartParser,FormParser
from myBlog.Utility.functionHelpers import validatePost
from django.contrib.auth.models import User
import time
# Create your views here.
@api_view(('GET',))
@permission_classes((AllowAny, ))
def demo(request):
    return Response({"msg":"test api"})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,FormParser)

    def list(self, request):
        posts = Post.objects.filter(user=request.user.pk)
        
        return Response(
            self.serializer_class(posts, many=True).data,
            status=status.HTTP_200_OK,
        )
    def retrieve(self, request, pk=None):
        if pk is not None:
            try:
                return Response(
                    self.serializer_class(Post.objects.get(pk=pk)).data, status=status.HTTP_200_OK
                )
            except:
                return Response({"msg": "Not found!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg":"Nothing"})
    def create(self, request):
        data = request.POST
        obj = {
            "user":data.get("user", False) if "user" in data else None,
            "content":data.get("content", False) if "content" in data else None,
            "file":request.FILES.get("file", False) if "file" in request.FILES else None,
        }
        # validate
        validate = validatePost(obj)
        
        if not validate[0]:
            return Response({"msg":validate[1]}, status=status.HTTP_400_BAD_REQUEST)
        # end validate

        # 
        user = User.objects.get(pk=obj["user"])
        
        if obj["file"] is None:
            post = Post.objects.create(user=user, content=obj["content"], like_count=0)
            post.save()
        else:
            file = obj["file"]
            file.name = "post_"+ str(obj["user"])+"_"+ date.today().strftime("%d%m%y")+"_" +str(round(time.time() * 1000))+ "." + file.name.split(".")[1].lower()
            post = Post.objects.create(user=user, content=obj["content"], like_count=0, image_url=file)
            post.save()
        
        return Response({"msg":"Created"}, status=201)
    def update(self, request, pk=None):
        if pk is not None:
            try:
                data = request.data
               
                obj = {
                    "user":data.get("user", False) if "user" in data else None,
                    "content":data.get("content", False) if "content" in data else None,
                    "file":request.FILES.get("file", False) if "file" in request.FILES else None,
                }
                
                # # validate
                validate = validatePost(obj, action="update")
                
                if not validate[0]:
                    return Response({"msg":validate[1]}, status=status.HTTP_400_BAD_REQUEST)
                # end validate
                
                #validate post
                try:
                    post = Post.objects.get(pk=pk)
                except Post.DoesNotExist:
                    return Response({"msg":"Post does not exist"}, status=status.HTTP_404_NOT_FOUND)


                post.content = obj["content"]
                if obj["file"] is not None:
                    post.image_url.delete()
                    file = obj["file"]
                    file.name = "post_"+ str(post.user.pk)+"_"+ date.today().strftime("%d%m%y")+"_" +str(round(time.time() * 1000))+ "." + file.name.split(".")[1].lower()
                    post.image_url = file
                post.save(update_fields=["user","content","image_url"])

                return Response({"msg":"Updated!"}, status=200)
            except:
                return Response({"msg": "Update fail!"}, status=status.HTTP_400_BAD_REQUEST)            
    def partial_update(self, request, pk=None):
        return Response({"msg": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        if pk is not None:
            try:
                try:
                    post = Post.objects.get(pk=pk)
                except Post.DoesNotExist:
                    return Response({"msg":"Post does not exist"}, status=status.HTTP_404_NOT_FOUND)
                if request.user.pk != post.user.pk:
                    return Response({"msg":"Only owner can delete their post!"}, status=status.HTTP_404_NOT_FOUND)
                post.image_url.delete()
                post.delete()
                return Response({"msg":"Delete post successfully"}, status=status.HTTP_200_OK)
            except:
                return Response({"msg": "Delete Fail"}, status=status.HTTP_404_NOT_FOUND)