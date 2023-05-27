from rest_framework import serializers
from .models import Post, Comment
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from users.serializers import UserProfileSerializer
from urllib.parse import urlsplit
from users.models import user


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


      



class GETPostSerializers(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Post
        fields = '__all__'


class LikeSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class GetCommentSerializer(serializers.ModelSerializer):
        user = UserProfileSerializer()
        class Meta:
            model = Comment
            fields = '__all__'

