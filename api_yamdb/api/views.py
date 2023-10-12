from rest_framework import viewsets, filters
from django_filters import FilterSet
from django_filters import CharFilter, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from api.serializers import CategorySerializer, TitleSerializer, GenreSerializer, CommentSerializer, ReviewSerializer
from categories.models import Categories
from genres.models import Genres
from titles.models import Titles, Review


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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Titles, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
