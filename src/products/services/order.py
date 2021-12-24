from django.shortcuts import get_object_or_404

from products.models import Order


def update_order(*, pk: int, **data) -> Order:
    order = get_object_or_404(Order, pk=pk)

    for attr, value in data.items():
        setattr(order, attr, value)

    order.save()

    return order
