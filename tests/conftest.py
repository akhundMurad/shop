import pytest

from products.factories import ProductFactory, OrderFactory


@pytest.fixture
def product(db) -> ProductFactory:
    return ProductFactory()


@pytest.fixture
def order(db) -> OrderFactory:
    return OrderFactory()
