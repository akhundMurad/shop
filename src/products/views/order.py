from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Order, Product
from ..services.order import update_order


class OrderPartialUpdateAPIView(APIView):
    class InputSerializer(serializers.Serializer):
        status = serializers.ChoiceField(choices=Order.Status.choices)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Order
            fields = ('id', 'status')

    serializer_class = InputSerializer

    def get_queryset(self) -> QuerySet:
        return Order.objects.get_queryset()

    @extend_schema(
        methods=['PATCH'],
        request=InputSerializer,
        responses={200: OutputSerializer},
    )
    def patch(self, request, *args, **kwargs) -> Response:
        serialized = self.InputSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        order = update_order(pk=kwargs['pk'], **serialized.validated_data)

        return Response(
            data=self.OutputSerializer(order).data, status=status.HTTP_200_OK
        )
