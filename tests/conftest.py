import pytest

from products.factories import ProductFactory


@pytest.fixture
def product(db) -> ProductFactory:
    return ProductFactory()
