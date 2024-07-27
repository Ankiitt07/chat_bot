from django.shortcuts import render
from rest_framework.views import APIView
from .models import CustomUsers
from .serializers import (
    UserRegisterSerializer,
    LoginSerializer,
    UserSerializer
)
from .utils import generate_tokens_for_user
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class RegisterUser(APIView):

    def post(self, request, format=None):

        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            access_token, refresh_token = generate_tokens_for_user(user)
            response = {
                "success": True,
                "message": f"User registered successfully",
                "data": {
                    "user": UserSerializer(user).data,
                    "access_token": str(access_token),
                    "refresh_token": str(refresh_token),
                },
            }
            return Response(response, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(APIView):

    def post(self, request, format=None):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            access_token, refresh_token = generate_tokens_for_user(user)
            response = {
                "success": True,
                "message": f"User login successfully",
                "data": {
                    "user": UserSerializer(user).data,
                    "access_token": str(access_token),
                    "refresh_token": str(refresh_token),
                },
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = {
                "success": True,
                "message": f"user logout successfully"
            }
            return Response(response, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserAuthentication(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        response = {
            "status" : True,
            "message" : "User is authenticated"
        }
        return Response(response, status = status.HTTP_200_OK)