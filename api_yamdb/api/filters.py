from django_filters import CharFilter, FilterSet, NumberFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category__slug', lookup_expr='iexact')
    genre = CharFilter(field_name='genre__slug', lookup_expr='iexact')
    name = CharFilter(lookup_expr='icontains')
    year = NumberFilter()

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
