from django.core.exceptions import ValidationError

from products.models import OrderedProduct
from products.services.order import create_order


def bulk_create(
        *, serializer, data: list[dict]
) -> list[OrderedProduct]:
    prepared_items, errors = get_prepared_items(data, serializer)

    if any(errors):
        raise ValidationError(errors)

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


def get_prepared_items(data: list[dict], serializer) -> tuple:
    prepared_objects = []
    errors = []

    if not isinstance(data, list):
        raise ValidationError('Request data must be an array.')

    for item in data:
        serialized = serializer(data=item)
        try:
            if serialized.is_valid(raise_exception=True):
                data = serialized.validated_data
                data.update({
                    'id': item.get('id', None)
                })
                instance = OrderedProduct(**data)
                prepared_objects.append(instance)
                errors.append({})
        except ValidationError as e:
            errors.append(e.get_full_details())

    return prepared_objects, errors
