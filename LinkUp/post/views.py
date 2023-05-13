from django.shortcuts import render
from .models import Post
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from users.models import user
from .models import Post
from .serializers import PostSerializers, GETPostSerializers
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
        usr = user.objects.get(pk = User)
        caption = request.data.get('caption')
        media_type = request.data.get('media_type')
        media_url = request.FILES.get('media_url')


        file_path = default_storage.save(media_url, ContentFile(media_url.read()))


        # saving post object without mediafile

        post = Post.objects.create(user = usr,caption=caption,media_type=media_type)

        post_id = post.post_id
        try:
            post = Post.objects.get(post_id=post_id)
            print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            compress_media.delay(post_id=post_id,media_url=file_path,file_name = media_url.name)
            print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
            return Response({'message': 'Media compression task queued successfully'})
        except Post.DoesNotExist:
            return Response({'error': f'Post with ID {post_id} does not exist'}, status=400)
        