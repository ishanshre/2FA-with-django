from rest_framework import status, generics

from .serializers import UserRegisterSerializer, UserViewSerializer, UserOtpSerializer

from rest_framework.response import Response
from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated


import pyotp
User = get_user_model()


class UserRegisterView(generics.GenericAPIView):
    """
    Register new user
    """
    serializer_class = UserRegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "status":"done",
            "message":"user created",
        }, status=status.HTTP_201_CREATED)


class UserView(generics.GenericAPIView):
    """
    view user info only for authenticated users
    """
    serializer_class = UserViewSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','head','options']

    def get(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.serializer_class(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenerateOtpSeretView(generics.GenericAPIView):
    """Generating otp secret and url for google authenticator"""
    serializer_class = UserViewSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(instance=user, data = request.data)
        serializer.is_valid(raise_exception=True)
        otp_base32 = pyotp.random_base32()
        otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
            name=user.username, issuer_name="Ishan Shrestha"
        )
        user.otp_base32 = otp_base32
        user.otp_auth_url = otp_auth_url
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyOtpView(generics.GenericAPIView):
    serializer_class = UserOtpSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post','options','head']

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(instance=user, data=request.data)
        serializer.context['otp_base32'] = user.otp_base32
        serializer.is_valid(raise_exception=True)
        user.otp_enabled = True
        user.otp_verified = True
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    