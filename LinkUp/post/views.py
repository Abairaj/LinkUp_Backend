from django.shortcuts import render
from .models import Post
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from users.models import user
from .models import Post, Comment
from .serializers import PostSerializers, GETPostSerializers, LikeSerializer, CommentSerializer, GetCommentSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .task import Compress_media


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class PostAPIView(APIView):
    pagination_class = PostPagination

    def get(self, request):
        paginator = self.pagination_class()
        posts = Post.objects.exclude(deleted=True).select_related(
            'user').order_by('-created_at')
        paginated_posts = paginator.paginate_queryset(posts, request)

        serializer = GETPostSerializers(paginated_posts, many=True)
        return paginator.get_paginated_response(serializer.data)


class PostByIdApiView(APIView):
    def get(self, request, user_id):
        posts = Post.objects.exclude(deleted=True).filter(
            user=user_id).order_by("-created_at")
        if posts:
            serializer = GETPostSerializers(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "no post yet"}, status=status.HTTP_404_NOT_FOUND)


class Create_Post_API_VIEW(APIView):

    def post(self, request, user_id):
        serializer = PostSerializers(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        print('////////////////////////////////////////////////////////////////////////////////')
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def patch(self, request, user_id):
        try:
            post = Post.objects.get(post_id=user_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        post.deleted = True
        post.save()
        print(post.deleted)
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_304_NOT_MODIFIED)


class Reels_API_VIEW(APIView):
    def get(self, request):

        post = Post.objects.filter(deleted=False).select_related('user').filter(
            media_type="Video").order_by("-created_at")

        if post:
            serializer = GETPostSerializers(post, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)


class Post_Like_Unlike_APIView(APIView):
    def get_user(self, user_id):
        try:
            user_obj = user.objects.get(pk=user_id)
            return user_obj
        except user.DoesNotExist:
            return None

    def post(self, request, user_id):
        serializer = LikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post_id = serializer.validated_data['post_id']

        try:
            post = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return Response('Post does not exist', status=status.HTTP_404_NOT_FOUND)

        user_obj = self.get_user(user_id)
        if not user_obj:
            return Response('User does not exist', status=status.HTTP_404_NOT_FOUND)

        if user_obj in post.likes.all():
            post.likes.remove(user_obj)
            message = 'Post Unliked'
        else:
            post.likes.add(user_obj)
            message = 'Post Liked'

        # Serialize the updated post object
        serializer = PostSerializers(post)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class Post_Comment(APIView):

    def get(self, request, post_id):
        print(post_id)
        comments = Comment.objects.select_related(
            'user').filter(post=post_id).order_by('created_at')
        print(comments, 'dddd/////////////////')

        # pagination for comments
        # paginator = Comment_pagination()
        # paginated_comments = paginator.paginate_queryset(comments,request)

        if comments:
            print('2,////////////////////////')
            serializer = GetCommentSerializer(comments, many=True)
            # response = paginator.get_paginated_response(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            print('3,/////////////////////////////')
            return Response({"message": "No comments yet"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        print(request.data)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "comment added"}, status=status.HTTP_201_CREATED)

        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        comment_id = request.data.get('comment_id')

        try:
            comment = Comment.objects.get(comment_id=comment_id)

        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class test(APIView):
    def post(rself, equest):
        res = Compress_media.delay(media_file='file')
        if not res.successful():
            return Response("task done", status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)
