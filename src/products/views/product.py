from django.db.models import QuerySet
from rest_framework import serializers, status
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework.response import Response

from ..models import Product


class ProductListAPIView(ListAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ('id', 'name', 'cost_price', 'price', 'quantity')

    def get_queryset(self) -> QuerySet:
        return Product.objects.get_queryset()

    def list(self, request, *args, **kwargs) -> Response:
        data = self.OutputSerializer(
            self.get_queryset(),
            many=True
        ).data

        return Response(data=data, status=status.HTTP_200_OK)
