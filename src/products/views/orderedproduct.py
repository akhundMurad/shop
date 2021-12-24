from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product, OrderedProduct
from products.services.orderedproduct import bulk_create
from utils.exceptions import ErrorHandlerMixin


class OrderedProductBulkCreateAPIView(ErrorHandlerMixin, APIView):
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

    def post(self, request) -> Response:
        ordered_products = bulk_create(
            data=request.data, serializer=self.InputSerializer
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data=self.OutputSerializer(ordered_products, many=True).data
        )
