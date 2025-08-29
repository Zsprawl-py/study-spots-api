import django_filters as filters
from .models import Spot

class SpotFilter(filters.FilterSet):
    quiet_min = filters.NumberFilter(field_name='quiet_level', lookup_expr='gte')
    min_rating = filters.NumberFilter(method='filter_min_rating')
    wifi = filters.BooleanFilter()
    outlets = filters.BooleanFilter()
    city = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Spot
        fields = ['wifi', 'outlets', 'city']

    def filter_min_rating(self, queryset, name, value):
        return queryset.filter(avg_rating__gte=value)