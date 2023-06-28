from rest_framework import serializers
from .models import Report
from users.models import user
from post.models import Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class ReportSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    reporting_user = UserSerializer()
    reported_user = UserSerializer()

    class Meta:
        model = Report
        fields = "__all__"


class CreateReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"
