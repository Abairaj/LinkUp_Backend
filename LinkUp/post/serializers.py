from rest_framework import serializers
from .models import Post
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from urllib.parse import urlsplit


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
        class Meta:
            model = Post
            fields = '__all__'