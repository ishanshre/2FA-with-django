from rest_framework import serializers

from django.contrib.auth import get_user_model

import pyotp

User = get_user_model()



class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True)
    c_password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['username','password','c_password']

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        c_password = attrs['c_password']
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"error":"user already exists"})
        if password != c_password:
            raise serializers.ValidationError({"error":"passowrd mismatch"})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'])
        user.set_password(validated_data["password"])
        user.save()
        return user
    

class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','otp_enabled','otp_verified','otp_base32','otp_auth_url']
        extra_kwargs = {
            'username': {'read_only': True},
            'email': {'read_only': True},
            'otp_enabled': {'read_only': True},
            'otp_verified': {'read_only': True},
            'otp_base32': {'read_only': True},
            'otp_auth_url': {'read_only': True},
        }


class UserOtpSerializer(serializers.ModelSerializer):
    otp_token = serializers.CharField(max_length=100, write_only=True)
    class Meta:
        model = User
        fields = ['id','username','otp_token','otp_enabled','otp_verified']
        extra_kwargs = {
            'username': {'read_only': True},
            'otp_enabled': {'read_only': True},
            'otp_verified': {'read_only': True},
        }
    
    def validate(self, attrs):
        otp_token = attrs['otp_token']
        otp_base32 = self.context['otp_base32']
        totp = pyotp.TOTP(otp_base32)
        if not totp.verify(otp_token):
            raise serializers.ValidationError({"error":"invalid otp token"})
        return attrs
        