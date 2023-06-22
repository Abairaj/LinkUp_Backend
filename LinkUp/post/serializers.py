from rest_framework import serializers
from .models import Post, Comment
from users.serializers import UserProfileSerializer
from users.models import user
from post.models import Post
from .helper import image_to_json, compressing_image, compressing_videos


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        media_type = validated_data['media_type']
        usr = validated_data['user']
        # instance = super().create(validated_data)

        if media_type == "Image":
            media_file = validated_data.pop('image')
            image_name = media_file.name
            instance = super().create(validated_data)

            compressed_image = compressing_image(media_file, image_name)
            instance.image = compressed_image
            instance.save()
            return instance
        elif media_type == "Video":
            media_file = validated_data.pop('video')
            image_name = media_file.name
            instance = super().create(validated_data)


            compressed_video = media_file
            if compressed_video:
                instance.video = compressed_video
                instance.save()
            return instance


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
