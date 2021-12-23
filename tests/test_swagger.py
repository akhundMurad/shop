def test_return_200(client):
    response = client.get('/schema/')

    assert response.status_code == 200
