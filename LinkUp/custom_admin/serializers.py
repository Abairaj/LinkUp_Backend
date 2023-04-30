from rest_framework import serializers
from users.models import user



class AdminLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)

    class Meta:
        model = user
        fields = ("email", "password")