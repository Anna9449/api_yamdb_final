from rest_framework import serializers
from titles.models import Review, Comment


from categories.models import Categories
from genres.models import Genres
from titles.models import Titles


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Titles
        fields = "__all__"


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
