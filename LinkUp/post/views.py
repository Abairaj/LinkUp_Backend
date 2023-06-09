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
from django.shortcuts import get_object_or_404


def get_post_of_following(user_id):
    try:
        usr = get_object_or_404(user, id=user_id)
    except user.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    posts = Post.objects.filter(user__in=usr.following.all())
    return posts


def infinite_scroll_filter(request, user_id=None):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')

    limit = int(limit)
    offset = int(offset)
    following_post = get_post_of_following(user_id)

    try:
        filter = request.GET.get('filter')
    except:
        filter = False
    if filter:
        if filter == 'home':
            post = following_post.exclude(deleted=True).select_related(
                'user').order_by('-created_at')
            posts = post[offset:offset+limit]

            postCount = post.count()
        elif filter == 'reels':
            post = following_post.exclude(deleted=True).filter(media_type='Video').select_related(
                'user').order_by('-created_at')
            posts = post[offset:offset+limit]

            postCount = post.count()

        elif filter == 'all':
            post = Post.objects.exclude(deleted=True).order_by('-created_at')
            posts = post[offset:offset+limit]
            postCount = post.count()

    return {'posts': posts, 'postCount': postCount}


class PostAPIView(APIView):

    def get(self, request, user_id=None):
        posts = infinite_scroll_filter(request, user_id)
        serializer = GETPostSerializers(posts['posts'], many=True)
        return Response({'post': serializer.data, 'postCount': posts['postCount']}, status=status.HTTP_200_OK)


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

        if comments:
            serializer = GetCommentSerializer(comments, many=True)
            # response = paginator.get_paginated_response(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
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
