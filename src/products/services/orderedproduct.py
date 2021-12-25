from django.core.exceptions import ValidationError

from products.models import OrderedProduct, Product
from products.services.order import create_order


def bulk_create(
        *, serializer, data: list[dict]
) -> list[OrderedProduct]:
    prepared_items = get_prepared_items(data, serializer)

    prepared_items = add_to_order(prepared_items)
    ordered_products = OrderedProduct.objects.bulk_create(prepared_items)

    return ordered_products


def add_to_order(ordered_products: list[OrderedProduct]) -> list:
    new_ordered_products = list()
    order = create_order(ordered_products)

    for product in ordered_products:
        product.order = order
        new_ordered_products.append(product)

    return new_ordered_products


def get_prepared_items(data: list[dict], serializer) -> list:
    prepared_objects = []

    if not isinstance(data, list):
        raise ValidationError('Request data must be an array.')

    for item in data:
        serialized = serializer(data=item)
        if serialized.is_valid(raise_exception=True):
            data = serialized.validated_data
            data.update({
                'id': item.get('id', None)
            })
            instance = OrderedProduct(**data)

            check_is_out_of_stock(
                product=instance.product,
                product_quantity=instance.product_quantity
            )

            prepared_objects.append(instance)

    return prepared_objects


def check_is_out_of_stock(product: Product, product_quantity: int) -> None:
    if product_quantity > product.quantity:
        raise ValidationError('Product is out of stock.')
