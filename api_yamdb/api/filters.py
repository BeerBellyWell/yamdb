from django_filters import rest_framework as filter

from reviews.models import Title


class SlugFilterInFilter(filter.BaseInFilter, filter.CharFilter):
    pass


class TitleFilter(filter.FilterSet):
    genre = SlugFilterInFilter(field_name='genre__slug', lookup_expr='in')
    category = SlugFilterInFilter(field_name='category__slug',
                                  lookup_expr='in')
    name = SlugFilterInFilter(field_name='name', lookup_expr='in')
    year = filter.BaseInFilter(field_name='year', lookup_expr='in')

    class Meta:
        Model = Title
        fields = ['genre', 'category', 'year', 'name']
