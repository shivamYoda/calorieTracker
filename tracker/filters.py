import django_filters
from .models import TrackerEntry
from django.db.models import Q



class TrackerFilter(django_filters.FilterSet):
    calories = django_filters.NumberFilter(field_name='calories', lookup_expr='exact')
    calories__gte = django_filters.NumberFilter(field_name='calories', lookup_expr='gte')
    calories__lte = django_filters.NumberFilter(field_name='calories', lookup_expr='lte')
    calories__ne = django_filters.CharFilter(method='not_equal_filter')
    user = django_filters.NumberFilter(field_name='user', lookup_expr='exact')
    id = django_filters.NumberFilter(field_name='id', lookup_expr='exact')
    text = django_filters.CharFilter(field_name='text', lookup_expr='exact')
    less_than_calories_per_day = django_filters.BooleanFilter(field_name='less_than_calories_per_day', lookup_expr='exact')
    time__gte = django_filters.TimeFilter(field_name='time', lookup_expr='gte')
    time__lte = django_filters.TimeFilter(field_name='time', lookup_expr='lte')
    time = django_filters.TimeFilter(field_name='time', lookup_expr='exact')
    date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date__lte = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    date = django_filters.DateFilter(field_name='date', lookup_expr='exact')

    def not_equal_filter(self, queryset, name, value):
        field = name.split("__")[0]
        kwargs = {}
        kwargs[str(field)] = value
        return queryset.filter(~Q(**kwargs))

    class Meta:
        model = TrackerEntry
        fields = ['calories', 'user', 'id', 'text', 'date', 'time', 'less_than_calories_per_day']