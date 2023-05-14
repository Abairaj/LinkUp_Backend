from django.shortcuts import render
from .models import Post
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from users.models import user
from .models import Post, Comment
from .serializers import PostSerializers, GETPostSerializers, LikeSerializer, CommentSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .task import compress_media


class PostAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, user_id):
        try:
            User = user.objects.get(pk=user_id)
            return User
        except:
            return Response(stateus=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        User = Post.objects.select_related('user').filter(user=user_id)
        if User:
            serializer = GETPostSerializers(User, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_302_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        User = self.kwargs.get('user_id')
        usr = user.objects.get(pk=User)
        caption = request.data.get('caption')
        media_type = request.data.get('media_type')
        media_url = request.FILES.get('media_url')

        file_path = default_storage.save(
            media_url, ContentFile(media_url.read()))

        # saving post object without mediafile

        post = Post.objects.create(
            user=usr, caption=caption, media_type=media_type, media_url=file_path)

        post_id = post.post_id
        try:
            post = Post.objects.get(post_id=post_id)
            print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            compress_media.delay(
                post_id=post_id, media_url=file_path, file_name=media_url.name)
            print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
            return Response({'message': 'Media compression task queued successfully'})
        except Post.DoesNotExist:
            return Response({'error': f'Post with ID {post_id} does not exist'}, status=400)


class Post_Like_Unlike_APIView(APIView):

    def post(self, request, user_id):
        serializer = LikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post_id = serializer.validated_data['post_id']

        try:
            post = Post.objects.get(post_id=post_id)

        except Post.DoesNotExist:
            return Response('Post does not exist', status=status.HTTP_404_NOT_FOUND)

        if user_id in post.likes.all():
            post.likes.remove(user_id)
            message = 'Post Unliked'
        else:
            post.likes.add(user_id)
            message = 'Post Liked'

        return Response({'message': message}, status=status.HTTP_201_CREATED)


class Post_Comment(APIView):

    def get(self,request):
        pass


    def post(self, request, user_id):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "comment added"}, status=status.HTTP_201_CREATED)

    def patch(self, request):
        serializer = CommentSerializer(data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    
    
