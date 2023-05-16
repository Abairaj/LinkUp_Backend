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

    def create(self, validated_data):
        user_id = self.context['user_id']
        image = self.context['image']
        storage = FileSystemStorage()

        image_name = storage.get_available_name(image)
        storage.save(image_name, File(image))
        url = storage.url(image_name)
        path = urlsplit(url).path

        return {'user_id': user_id, 'path': path, 'file_name': image_name}


class GETPostSerializers(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Post
        fields = '__all__'


class LikeSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()


class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializers()
    user = UserProfileSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class GetCommentSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
