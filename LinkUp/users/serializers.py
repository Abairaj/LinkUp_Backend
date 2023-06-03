from rest_framework import serializers
from .models import user
from post.models import Post


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ("username", "email", "full_name", "password")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)

    class Meta:
        model = user
        fields = ("email", "password")

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    username = serializers.CharField()
    full_name = serializers.CharField()
    profile = serializers.ImageField(required=False)
    gender = serializers.CharField(allow_blank=True)
    phone = serializers.RegexField(regex=r'^\d{10}$')
    bio = serializers.CharField(allow_blank=True)
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    following = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    class Meta:
        model = user
        fields = ('id', 'email', 'username', 'full_name', 'profile', 'gender',
                  'phone', 'bio', 'followers','following', 'created_at', 'last_login')


class UserFollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, validated_data):
        usr = validated_data
        try:
            user_to_follow = user.objects.get(id=usr)
        except user.DoesNotExist:
            raise serializers.ValidationError("Invalid user ID")

        return user_to_follow


class UserUnfollowSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = user
        fields = ("following",)

    def validate_user_id(self, user_id):
        try:
            User = user.objects.get(id=value)
            print(User, 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid user ID")
        print(validated_data, 'kkkkkkkkkkkkkkkkkkkkkkkkk')

        return user

    def update(self, instance, validated_data):
        user_to_unfollow = validated_data['user_id']
        instance.followers.remove(user_to_unfollow)
        return instance
