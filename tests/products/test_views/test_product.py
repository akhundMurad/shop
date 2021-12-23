import pytest
from rest_framework.reverse import reverse


@pytest.fixture
def list_url() -> str:
    return reverse('products:product-list')


class TestProductListAPIView:
    def test_return_200(self, list_url, client, product, db):
        response = client.get(list_url)

        assert response.status_code == 200

    def test_return_data(self, list_url, client, product, db):
        response = client.get(list_url)
        item: dict = response.data[0]

        assert 'id' in item
        assert 'name' in item
        assert 'cost_price' in item
        assert 'price' in item
        assert 'quantity' in item

        assert isinstance(item['id'], int)
        assert isinstance(item['name'], str)
        assert isinstance(item['cost_price'], int)
        assert isinstance(item['price'], int)
        assert isinstance(item['quantity'], int)
