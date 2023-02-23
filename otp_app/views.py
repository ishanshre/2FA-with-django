from rest_framework import status, generics

from .serializers import UserRegisterSerializer

from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "status":"done",
            "message":"user created",
        }, status=status.HTTP_201_CREATED)
