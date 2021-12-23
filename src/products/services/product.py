from products.models import Product


def create_product(**data) -> Product:
    product = Product(**data)
    product.full_clean()
    product.save()

    return product
