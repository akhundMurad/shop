from datetime import timedelta

import pytest
import time_machine
from django.utils import timezone
from rest_framework.reverse import reverse

from reporting.factories import ReportFactory


TODAY = timezone.now().date()


@pytest.fixture
def last_week_report(product) -> ReportFactory:
    with time_machine.travel(TODAY - timedelta(weeks=1)):
        return ReportFactory(product=product)


@pytest.fixture
def report(product) -> ReportFactory:
    return ReportFactory(product=product)


@pytest.fixture
def list_url() -> str:
    return reverse('reporting:report-list')


class TestReportListAPIView:
    def test_return_200(self, client, db, list_url):
        response = client.get(list_url)

        assert response.status_code == 200

    def test_return_data(self, client, db, report, list_url):
        response = client.get(list_url)
        item = response.data[0]

        assert 'id' in item
        assert 'product' in item
        assert 'proceeds' in item
        assert 'earnings' in item
        assert 'number_of_sold' in item
        assert 'number_of_canceled' in item
        assert 'created_at' in item

        assert isinstance(item['id'], int)
        assert isinstance(item['product'], int)
        assert isinstance(item['proceeds'], int)
        assert isinstance(item['earnings'], int)
        assert isinstance(item['number_of_sold'], int)
        assert isinstance(item['number_of_canceled'], int)
        assert isinstance(item['created_at'], str)

    def test_filters(self, client, report, last_week_report, db, list_url):
        response = client.get(list_url, {
            'start_date': TODAY - timedelta(days=1),
            'end_date': TODAY + timedelta(days=1)
        })
        data = [item['id'] for item in response.data]

        assert len(data) == 1
        assert report.id in data
