from django.db.models import QuerySet
from django_filters.rest_framework import FilterSet, filters

from reporting.models import Report


class ReportFilterSet(FilterSet):
    start_date = filters.DateFilter(
        lookup_expr='gte',
        field_name='created_at'
    )
    end_date = filters.DateFilter(
        lookup_expr='lte',
        field_name='created_at'
    )

    class Meta:
        model = Report
        fields = ('start_date', 'end_date')


def list_report(filters_data=None) -> QuerySet:
    filters_data = filters_data or {}

    reports = Report.objects.select_related('product')

    return ReportFilterSet(data=filters_data, queryset=reports).qs
