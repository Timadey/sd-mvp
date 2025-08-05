from django.contrib.auth.models import update_last_login

from .models import User
from .dtos import CreateUserDTO, LoginDTO
from django.contrib.auth.hashers import make_password
from api.core.exceptions.exceptions import ConflictException
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from api.core.exceptions.exceptions import UnauthorizedException
from .serializers import UserBaseSerializer


class UserService:
    @staticmethod
    def create_user(dto: CreateUserDTO) -> User:
        if User.objects.filter(username=dto.username).exists():
            raise ConflictException("Username already exists")

        return User.objects.create(
            first_name=dto.first_name,
            last_name=dto.last_name,
            username=dto.username,
            password=make_password(dto.password),
            email=dto.email,
            role=dto.role
        )

    @staticmethod
    def authenticate_user(dto: LoginDTO):
        user = authenticate(username=dto.username, password=dto.password)
        if not user:
            raise UnauthorizedException("Invalid credentials")

        refresh = RefreshToken.for_user(user)
        update_last_login(None, user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "access_lifetime" : refresh.access_token.lifetime,
            "refresh_lifetime": refresh.lifetime,
            "user" : UserBaseSerializer(user).data
        }
