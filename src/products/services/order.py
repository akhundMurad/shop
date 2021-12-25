from django.shortcuts import get_object_or_404

from products.models import Order


def create_order(ordered_products: list) -> Order:
    order = Order(
        status=Order.Status.ON_PROCESSING,
        products_quantity=_get_products_quantity(ordered_products),
        total_cost_price=_get_total_cost_price(ordered_products),
        total_price=_get_total_price(ordered_products)
    )
    
    order.full_clean()
    order.save()
    return order


def _get_products_quantity(ordered_products: list) -> int:
    products_quantity = 0
    for item in ordered_products:
        products_quantity += item.product_quantity
    
    return products_quantity


def _get_total_cost_price(ordered_products: list) -> int:
    total_cost_price = 0
    for item in ordered_products:
        total_cost_price += item.product.cost_price

    return total_cost_price


def _get_total_price(ordered_products: list) -> int:
    total_price = 0
    for item in ordered_products:
        total_price += item.product.price

    return total_price


def update_order(*, pk: int, **data) -> Order:
    order = get_object_or_404(Order, pk=pk)

    for attr, value in data.items():
        setattr(order, attr, value)

    order.save()

    return order
