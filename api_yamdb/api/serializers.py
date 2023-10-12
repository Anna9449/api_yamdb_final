from datetime import datetime

from rest_framework import serializers
from titles.models import Review, Comment


from categories.models import Categories
from genres.models import Genres
from titles.models import Titles


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Titles
        fields = "__all__"

    def validate_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError('Год выпуска не может быть больше текущего')
        return value

    def validate_genre(self, value):
        for genre in value:
            genre = Genres.objects.get(slug=genre)
            if not genre:
                raise serializers.ValidationError("Нельзя добавить произведение с несуществующим жанром")
        return value

    def validate_category(self, value):
        category = Categories.objects.get(slug=value)
        if not category:
            raise serializers.ValidationError("Нельзя добавить произведение с несуществующей категорией")
        return value


    def create(self, validated_data):
        user = self.context['request'].user
        if not user.admin:
            raise serializers.ValidationError('Произведение может добавить только Админ')
        super().create(validated_data)




class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
        read_only_fields = ('review',)

