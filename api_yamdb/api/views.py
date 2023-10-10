from rest_framework import viewsets, filters
from django_filters import FilterSet
from django_filters import CharFilter, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response

from api.serializers import CategorySerializer, TitleSerializer, GenreSerializer
from categories.models import Categories
from genres.models import Genres
from titles.models import Titles


class TitleFilter(FilterSet):
    category = CharFilter(field_name="category__slug", lookup_expr="iexact")
    genre = CharFilter(field_name="genre__slug", lookup_expr="iexact")
    name = CharFilter(lookup_expr="icontains")
    year = NumberFilter()

    class Meta:
        model = Titles
        fields = ["category", "genre", "name", "year"]


class CustomListViewMixin:
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "count": len(serializer.data),
            "next": "string",  # Пока не понимаю что сюда вставить надо
            "previous": "string",  # Пока не понимаю что сюда вставить надо
            "results": serializer.data,
        }
        return Response(data)


class TitleViewSet(CustomListViewMixin, viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_class = TitleFilter


class GenreViewSet(CustomListViewMixin, viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class CategoryViewSet(CustomListViewMixin, viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
