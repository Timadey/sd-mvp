from rest_framework import serializers

from api.users.models import User


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role']

class UserCreateSerializer(UserBaseSerializer):
    password = serializers.CharField(write_only=True)

    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + ['password']
