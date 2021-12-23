from django.db.models import QuerySet
from rest_framework import serializers, status
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework.response import Response

from ..models import Product
from ..services.product import create_product, update_product


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


class ProductCreateAPIView(CreateAPIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        cost_price = serializers.IntegerField()
        price = serializers.IntegerField()
        quantity = serializers.IntegerField()

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ('id', 'name', 'cost_price', 'price', 'quantity')

    def create(self, request, *args, **kwargs) -> Response:
        serialized = self.InputSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        product = create_product(**serialized.validated_data)

        return Response(
            data=self.OutputSerializer(product).data,
            status=status.HTTP_201_CREATED
        )


class ProductPartialUpdateAPIView(UpdateAPIView):
    class InputSerializer(serializers.Serializer):
        cost_price = serializers.IntegerField(required=False)
        price = serializers.IntegerField(required=False)
        quantity = serializers.IntegerField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ('id', 'name', 'cost_price', 'price', 'quantity')

    def get_queryset(self) -> QuerySet:
        return Product.objects.get_queryset()

    def partial_update(self, request, *args, **kwargs) -> Response:
        serialized = self.InputSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        product = update_product(pk=kwargs['pk'], **serialized.validated_data)

        return Response(
            data=self.OutputSerializer(product).data,
            status=status.HTTP_200_OK
        )
