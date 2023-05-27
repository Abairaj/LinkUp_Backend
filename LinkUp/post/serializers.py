from rest_framework import serializers
from .models import Post, Comment
from users.serializers import UserProfileSerializer
from users.models import user
from PIL import Image
from io import BytesIO
from django.core.files import File



class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

        def create(self,validated_data):
            image = validated_data["media_url"]
            media_type = validated_data["media_type"]
            if media_type == "Image":
                img = Image.open(image)
                img_io = BytesIO()
                image.save(img_io,'jpeg',quality=50)
                new_image = File(img_io,name=image.name)
                return new_image



      



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

