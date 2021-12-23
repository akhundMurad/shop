from django.shortcuts import get_object_or_404

from products.models import Product


def create_product(**data) -> Product:
    product = Product(**data)
    product.full_clean()
    product.save()

    return product


def update_product(*, pk: int, **data) -> Product:
    product = get_object_or_404(Product, pk=pk)

    for attr, value in data.items():
        setattr(product, attr, value)

    product.save()

    return product
