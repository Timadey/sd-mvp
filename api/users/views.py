from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView

from api.core.responses import success
from api.users.dtos import CreateUserDTO, LoginDTO
from api.users.serializers import UserCreateSerializer, UserBaseSerializer
from api.users.services import UserService

class RegisterView(APIView):
    @extend_schema(
        tags=["Auth"],
        request=UserCreateSerializer,
        responses=OpenApiResponse(response=UserCreateSerializer, description="Create a new user"),
    )
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print(serializer.validated_data)

        dto = CreateUserDTO(**serializer.validated_data)
        user = UserService.create_user(dto)

        return success(UserCreateSerializer(user).data, "User registered successfully", status=status.HTTP_201_CREATED)


class LoginView(APIView):
    @extend_schema(
        tags=["Auth"],
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "example": "john.doe/john.doe@example.com"},
                    "password": {"type": "string", "example": "secret123"}
                },
                "required": ["username", "password"]
            }
        },
        responses={
            200: OpenApiResponse(description="Login using username or email address"),
        },
    )
    def post(self, request):
        try:
            dto = LoginDTO(
                username=request.data.get("username"),
                password=request.data.get("password")
            )
            tokens = UserService.authenticate_user(dto)
            return success(tokens, "User logged in successfully")
        except Exception as e:
            raise e

class RefreshTokenView(TokenRefreshView):
    @extend_schema(
        tags=["Auth"],
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "refresh": {"type": "string", "example": "<jwt-refresh-token>"}
                },
                "required": ["refresh"]
            }
        },
        responses={
            200: OpenApiResponse(description="Token refreshed successfully"),
            401: OpenApiResponse(description="Invalid refresh token"),
        },
    )
    def post(self, request, *args, **kwargs):
        try:
            refresh = request.data.get("refresh", None)
            if refresh is None:
                raise InvalidToken("No refresh token provided")

            response = super().post(request, *args, **kwargs)
            return success(response.data, "Token refreshed successfully")

        except InvalidToken as e:
            raise e

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Auth"],
        responses=OpenApiResponse(response=UserBaseSerializer, description="Authenticated user info"),
    )
    def get(self, request):
        user = request.user
        return success(UserBaseSerializer(user).data, "User details retrieved successfully")