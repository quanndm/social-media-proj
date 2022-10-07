from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from rest_framework import viewsets,status
from .models import Post
from .serializers import PostSerializer
from rest_framework.parsers import MultiPartParser,FormParser
# Create your views here.
@api_view(('GET',))
@permission_classes((AllowAny, ))
def demo(request):
    return Response({"msg":"test api"})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser,FormParser)

    def list(self, request):
        return Response(
            self.serializer_class(self.queryset, many=True).data,
            status=status.HTTP_200_OK,
        )
    def retrieve(self, request, pk=None):
        if pk is not None:
            try:
                self.queryset = Post.objects.get(pk=pk)
                return Response(
                    self.serializer_class(self.queryset).data, status=status.HTTP_200_OK
                )
            except:
                return Response({"msg": "Nothing"})
        return Response({"msg":"Nothing"})
    def create(self, request):
        data = request.data
        print(data)
        
        return Response({"msg":"Created"})