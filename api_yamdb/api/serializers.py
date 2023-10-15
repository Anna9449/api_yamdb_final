import re
from datetime import datetime

from rest_framework import serializers

from categories.models import Categories
from genres.models import Genres
from reviews.models import Comment, Review, Title
from users.models import MyUser


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        queryset=Genres.objects.all(),
        slug_field="slug"
    )

    category = serializers.SlugRelatedField(
        read_only=False,
        queryset=Categories.objects.all(),
        slug_field="slug"
    )

    class Meta:
        model = Title
        fields = "__all__"

    def validate_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего'
            )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ("name", "slug")
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ("name", "slug")
        lookup_field = 'slug'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        exclude = ('title', )
        read_only_fields = ('title',)

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError(
                'Выберите оценку от 1 до 10!'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ('review',)
        read_only_fields = ('review',)


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
