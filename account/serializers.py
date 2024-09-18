from rest_framework import serializers
from .models import CustomUser

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class VerifyPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
