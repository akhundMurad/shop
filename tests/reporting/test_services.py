from datetime import timedelta

import pytest
import time_machine
from django.utils import timezone

from products.factories import OrderedProductFactory, OrderFactory
from products.models import Order
from reporting.models import Report
from reporting.services import create_reports

TODAY = timezone.now()


@pytest.fixture
def yesterday_order() -> OrderFactory:
    with time_machine.travel(TODAY - timedelta(days=1)):
        return OrderFactory(
            status=Order.Status.ON_PROCESSING
        )


@pytest.fixture
def today_order() -> OrderFactory:
    return OrderFactory(
        status=Order.Status.ON_PROCESSING,
        created_at=TODAY
    )


@pytest.fixture
def canceled_order() -> OrderFactory:
    return OrderFactory(
        status=Order.Status.CANCELED,
        created_at=TODAY
    )


@pytest.fixture
def yesterday_ordered_product(
        yesterday_order, product
) -> OrderedProductFactory:
    return OrderedProductFactory(
        order=yesterday_order,
        product=product
    )


@pytest.fixture
def ordered_product(today_order, product) -> OrderedProductFactory:
    return OrderedProductFactory(
        order=today_order,
        product=product
    )


@pytest.fixture
def ordered_product_1(canceled_order, product) -> OrderedProductFactory:
    return OrderedProductFactory(
        order=canceled_order,
        product=product
    )


@pytest.fixture
def create_reports_service(canceled_order, yesterday_ordered_product,
                           ordered_product, ordered_product_1):
    create_reports()


class TestCreateReports:
    def test_reports_created(self, product, create_reports_service):
        assert Report.objects.filter(
            product_id=product.id
        ).count() == 1

    def test_reports_data(self, product, ordered_product,
                          create_reports_service):
        report = Report.objects.get(
            product_id=product.id
        )
        proceeds = product.price * ordered_product.product_quantity
        earnings = proceeds - (
                product.cost_price * ordered_product.product_quantity
        )

        number_of_sold = 2
        number_of_canceled = 1

        assert report.proceeds == proceeds
        assert report.earnings == earnings
        assert report.number_of_sold == number_of_sold
        assert report.number_of_canceled == number_of_canceled
