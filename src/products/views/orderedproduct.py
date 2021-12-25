from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from products.models import Product, OrderedProduct
from products.services.orderedproduct import bulk_create


class OrderedProductBulkCreateAPIView(CreateAPIView):
    class InputSerializer(serializers.Serializer):
        product = serializers.PrimaryKeyRelatedField(
            queryset=Product.objects.all()
        )
        product_quantity = serializers.IntegerField()

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderedProduct
            fields = ('id', 'product', 'order', 'product_quantity')

    model = OrderedProduct

    def get_queryset(self) -> QuerySet:
        return OrderedProduct.objects.get_queryset()

    @extend_schema(
        methods=['POST'],
        request=InputSerializer,
        responses={201: OutputSerializer},
    )
    def create(self, request, *args, **kwargs) -> Response:
        ordered_products = bulk_create(
            data=request.data, serializer=self.InputSerializer
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data=self.OutputSerializer(ordered_products, many=True).data
        )
