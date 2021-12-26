from django.db.models import QuerySet
from rest_framework import serializers, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from reporting.models import Report
from reporting.selectors.report import list_report


class ReportListAPIView(ListAPIView):
    class FilterSerializer(serializers.Serializer):
        start_date = serializers.DateField(required=False)
        end_date = serializers.DateField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Report
            fields = ('id', 'product', 'proceeds', 'earnings',
                      'number_of_sold', 'number_of_canceled', 'created_at')

    def get_queryset(self, filters=None) -> QuerySet:
        return list_report(filters)

    def list(self, request, *args, **kwargs) -> Response:
        filters_serializer = self.FilterSerializer(
            data=request.query_params
        )
        filters_serializer.is_valid(raise_exception=True)

        data = self.OutputSerializer(
            self.get_queryset(
                filters=filters_serializer.validated_data
            ),
            context={'request': self.request},
            many=True
        ).data

        return Response(data=data, status=status.HTTP_200_OK)
