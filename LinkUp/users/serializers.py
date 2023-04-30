from rest_framework import serializers
from .models import user


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ("username", "email","full_name", "password")
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


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    full_name = serializers.CharField()
    profile = serializers.ImageField(required=False)
    gender = serializers.CharField(allow_blank=True)
    phone = serializers.RegexField(regex=r'^\d{10}$')
    bio = serializers.CharField(allow_blank=True)
    followers = serializers.IntegerField(read_only=True)
    following = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    class Meta:
        model = user
        fields = ('email', 'username', 'full_name', 'profile', 'gender',
                  'phone', 'bio', 'followers', 'following', 'created_at', 'last_login')
