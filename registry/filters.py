import django_filters
from .models import LateEntry

class LateEntryFilter(django_filters.FilterSet):
    # Exact date or range
    date = django_filters.DateFilter(field_name='date', lookup_expr='exact')
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    # Student-related fields
    roll_no = django_filters.CharFilter(field_name='student__roll_no', lookup_expr='exact')
    year = django_filters.NumberFilter(field_name='student__year', lookup_expr='exact')
    branch = django_filters.CharFilter(field_name='student__branch', lookup_expr='iexact')
    course = django_filters.CharFilter(field_name='student__course', lookup_expr='iexact')

    class Meta:
        model = LateEntry
        fields = ['date', 'start_date', 'end_date', 'roll_no', 'year', 'branch', 'course']
