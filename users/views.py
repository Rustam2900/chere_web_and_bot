from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser
from users.serializers import UserRegisterSerializer, UserLoginSerializer, UserProfileSerializer


class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = CustomUser.objects.all()

    def perform_create(self, serializer):
        password = serializer.validated_data.get('password')
        hashed_password = make_password(password)
        serializer.save(password=hashed_password)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginAPIView(CreateAPIView):
    throttle_classes = []
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if user:
            token = RefreshToken.for_user(user)
            data = serializer.data
            data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(RetrieveUpdateAPIView):
    throttle_classes = []
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
