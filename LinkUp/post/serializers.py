from rest_framework import serializers
from .models import Post, Comment
from users.serializers import UserProfileSerializer
from users.models import user
from post.models import Post
from .helper import compressing_image, compressing_videos


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        media_file = validated_data.pop('media_url')
        media_type = validated_data['media_type']
        usr = validated_data['user']
        instance = super().create(validated_data)
        image_name = media_file.name

        if media_type == "Image":
            compressed_image = compressing_image(media_file, image_name)
            print(compressed_image, '/////////////////////////////')
            instance.media_url = compressed_image
            instance.save()
            return instance
        elif media_type == "Video":
            compressed_video = compressing_videos(media_file)
            if compressed_video:
                print(compressed_video, '////////////////////////////')
                instance.media_url = compressed_video
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
