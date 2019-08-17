import django_filters
from .models import TrackerUser
from django.db.models import Q

class TrackerUserFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name='user', lookup_expr='exact')
    type = django_filters.CharFilter(field_name='type', lookup_expr='exact')
    expected_calories_per_day = django_filters.NumberFilter(field_name='expected_calories_per_day', lookup_expr='exact')
    expected_calories_per_day__gte = django_filters.NumberFilter(field_name='expected_calories_per_day__gte', lookup_expr='gte')
    expected_calories_per_day__lte = django_filters.NumberFilter(field_name='expected_calories_per_day__lte', lookup_expr='lte')

    def not_equal_filter(self, queryset, name, value):
        field = name.split("__")[0]
        kwargs = {}
        kwargs[str(field)] = value
        return queryset.filter(~Q(**kwargs))

    class Meta:
        model = TrackerUser
        fields = ['user', 'id', 'type', 'expected_calories_per_day']