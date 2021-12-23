import pytest
from rest_framework.reverse import reverse

from products.factories import ProductFactory


@pytest.fixture
def list_url() -> str:
    return reverse('products:product-list')


@pytest.fixture
def create_url() -> str:
    return reverse('products:product-create')


@pytest.fixture
def partial_update_url(product) -> str:
    return reverse(
        'products:product-partial-update', kwargs={'pk': product.id}
    )


@pytest.fixture
def product_data() -> dict:
    product = ProductFactory.build()
    return {
        'name': product.name,
        'cost_price': product.cost_price,
        'price': product.price,
        'quantity': product.quantity,
    }


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


class TestProductCreateAPIView:
    def test_return_201(self, create_url, client, product_data, db):
        response = client.post(create_url, product_data)

        assert response.status_code == 201

    def test_return_data(self, create_url, client, product_data, db):
        response = client.post(create_url, product_data)

        assert 'id' in response.data
        assert 'name' in response.data
        assert 'cost_price' in response.data
        assert 'price' in response.data
        assert 'quantity' in response.data

        assert isinstance(response.data['id'], int)
        assert isinstance(response.data['name'], str)
        assert isinstance(response.data['cost_price'], int)
        assert isinstance(response.data['price'], int)
        assert isinstance(response.data['quantity'], int)


class TestProductPartialUpdateAPIView:
    def test_return_200(self, partial_update_url, client, db):
        response = client.patch(partial_update_url, data={
            'name': 'asdas'
        }, content_type='application/json')

        assert response.status_code == 200

    def test_return_data(self, partial_update_url, client, db):
        response = client.patch(partial_update_url, {
            'name': 'asdas'
        }, content_type='application/json')

        assert 'id' in response.data
        assert 'name' in response.data
        assert 'cost_price' in response.data
        assert 'price' in response.data
        assert 'quantity' in response.data

        assert isinstance(response.data['id'], int)
        assert isinstance(response.data['name'], str)
        assert isinstance(response.data['cost_price'], int)
        assert isinstance(response.data['price'], int)
        assert isinstance(response.data['quantity'], int)
