import pytest
from flask.testing import FlaskClient
from ej2a2 import create_app

@pytest.fixture
def client() -> FlaskClient:
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

def test_get_product_exists(client):
    """Test GET /product/1 (product exists, should return 200)"""
    response = client.get("/product/1")
    assert response.status_code == 200
    assert response.json == {"id": 1, "name": "Laptop", "price": 999.99}

def test_get_product_exists_2(client):
    """Test GET /product/2 (product exists, should return 200)"""
    response = client.get("/product/2")
    assert response.status_code == 200
    assert response.json == {"id": 2, "name": "Smartphone", "price": 699.99}

def test_get_product_not_found(client):
    """Test GET /product/999 (product doesn't exist, should return 404)"""
    response = client.get("/product/999")
    assert response.status_code == 404
    assert "error" in response.json
