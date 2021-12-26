import pytest

from products.factories import ProductFactory, OrderFactory
from products.models import Order


@pytest.fixture
def product(db) -> ProductFactory:
    return ProductFactory()


@pytest.fixture
def order(db) -> OrderFactory:
    return OrderFactory(status=Order.Status.ON_PROCESSING)
