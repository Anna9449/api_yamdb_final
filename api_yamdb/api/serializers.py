from rest_framework import serializers

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
