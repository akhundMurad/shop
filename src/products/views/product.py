from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Product
from ..services.product import create_product, update_product


class ProductListAPIView(ListAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ('id', 'name', 'cost_price', 'price', 'quantity')

    serializer_class = OutputSerializer

    def get_queryset(self) -> QuerySet:
        return Product.objects.get_queryset()

    @extend_schema(
        methods=['GET'],
        responses={200: OutputSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs) -> Response:
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

    serializer_class = InputSerializer

    @extend_schema(
        methods=['POST'],
        request=InputSerializer,
        responses={201: OutputSerializer}
    )
    def post(self, request, *args, **kwargs) -> Response:
        serialized = self.InputSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        product = create_product(**serialized.validated_data)

        return Response(
            data=self.OutputSerializer(product).data,
            status=status.HTTP_201_CREATED
        )


class ProductPartialUpdateAPIView(APIView):
    class InputSerializer(serializers.Serializer):
        cost_price = serializers.IntegerField(required=False)
        price = serializers.IntegerField(required=False)
        quantity = serializers.IntegerField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ('id', 'name', 'cost_price', 'price', 'quantity')

    serializer_class = InputSerializer

    def get_queryset(self) -> QuerySet:
        return Product.objects.get_queryset()

    @extend_schema(
        methods=['PATCH', 'PUT'],
        request=InputSerializer,
        responses={201: OutputSerializer}
    )
    def patch(self, request, *args, **kwargs) -> Response:
        serialized = self.InputSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        product = update_product(pk=kwargs['pk'], **serialized.validated_data)

        return Response(
            data=self.OutputSerializer(product).data,
            status=status.HTTP_200_OK
        )
