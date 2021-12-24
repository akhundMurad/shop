from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.response import Response

from ..models import Order, Product


class OrderCreateAPIView(CreateAPIView):
    class InputSerializer(serializers.Serializer):
        products = serializers.PrimaryKeyRelatedField(
            many=True,
            queryset=Product.objects.all()
        )

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Order
            fields = ()

    def get_queryset(self) -> QuerySet:
        return Order.objects.get_queryset()

    def create(self, request, *args, **kwargs) -> Response:
        pass
