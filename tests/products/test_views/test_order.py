import pytest
from rest_framework.reverse import reverse

from products.models import Order


@pytest.fixture
def partial_update_url(order) -> str:
    return reverse('products:order-partial-update', kwargs={'pk': order.id})


class TestOrderPartialUpdateAPIView:
    def test_return_200(self, client, partial_update_url, db):
        response = client.patch(
            partial_update_url,
            data={'status': Order.Status.CANCELED},
            content_type='application/json'
        )

        assert response.status_code == 200

    def test_return_data(self, client, partial_update_url, db):
        response = client.patch(
            partial_update_url,
            data={'status': Order.Status.CANCELED},
            content_type='application/json'
        )

        assert 'id' in response.data
        assert 'status' in response.data

        assert isinstance(response.data['id'], int)
        assert isinstance(response.data['status'], str)
        assert response.data['status'] == Order.Status.CANCELED
