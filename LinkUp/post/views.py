from django.shortcuts import render
from .models import Post
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from users.models import user
from .serializers import PostSerializers,GETPostSerializers
from post.task import process_Post


class PostAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self,user_id):
        try:
            User = user.objects.get(pk=user_id)
            return User
        except:
            return Response(stateus = status.HTTP_404_NOT_FOUND)
        
    
    def get(self,request,user_id):
        User = self.get_object(user_id)
        if User:
            serializer = GETPostSerializers(User)
            return Response({"data":serializer.data},status=status.HTTP_302_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')

        image = request.FILES.get('media_url')

        serializer = PostSerializers(data=request.data, context={
            'user_id': user_id,
            'image': image
        })

        if serializer.is_valid():
            data = serializer.create(validated_data=request.data)
            task = process_Post.delay(
                user_id=data['user_id'],
                path=data['path'],
                file_name=data['file_name']
            )

            return Response('upload started...')
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

