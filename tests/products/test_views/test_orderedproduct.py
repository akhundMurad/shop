import pytest
from rest_framework.reverse import reverse


@pytest.fixture
def bulk_create_url() -> str:
    return reverse('products:ordered-product-bulk-create')


class TestOrderedProductBulkCreateAPIView:
    def test_return_201(self, client, bulk_create_url, product, db):
        response = client.post(
            bulk_create_url,
            data=[
                {
                    'product': product.id,
                    'product_quantity': product.quantity - 1
                }
            ],
            content_type='application/json'
        )

        assert response.status_code == 201, response.data

    def test_send_not_list(self, client, bulk_create_url, product, db):
        response = client.post(
            bulk_create_url,
            data={
                'product': product.id,
                'product_quantity': product.quantity - 1
            },
            content_type='application/json'
        )

        assert response.status_code == 400

    def test_product_is_out_of_stock(self, client,
                                     bulk_create_url, product, db):
        response = client.post(
            bulk_create_url,
            data=[
                {
                    'product': product.id,
                    'product_quantity': product.quantity + 1
                }
            ],
            content_type='application/json'
        )

        assert response.status_code == 400

    def test_return_data(self, client, bulk_create_url, product, db):
        response = client.post(
            bulk_create_url,
            data=[
                {
                    'product': product.id,
                    'product_quantity': product.quantity - 1
                }
            ],
            content_type='application/json'
        )
        item = response.data[0]

        assert 'id' in item
        assert 'order' in item
        assert 'product' in item
        assert 'product_quantity' in item

        assert isinstance(item['id'], int)
        assert isinstance(item['order'], int)
        assert isinstance(item['product'], int)
        assert isinstance(item['product_quantity'], int)

        assert item['product'] == product.id
        assert item['product_quantity'] == product.quantity - 1
