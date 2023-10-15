import re

from rest_framework import serializers

from users.models import MyUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = MyUser
        fields = ('username', 'confirmation_code')


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = MyUser
        fields = ('username', 'email')

    def validate(self, data):
        pattern = r'^[\w.@+-]+$'
        if data['username'] == 'me':
            raise serializers.ValidationError("Invalid username.")
        if len(data['username']) > 150:
            raise serializers.ValidationError(
                "Username is too long (maximum 150 characters).")
        if not re.match(pattern, data['username']):
            raise serializers.ValidationError("Invalid username format.")
        if len(data['email']) > 254:
            raise serializers.ValidationError(
                "Email is too long (maximum 254 characters).")
        return data
