import pytest
import threading
import requests
import time
import json
from ej2a2 import create_server

@pytest.fixture
def server():
    """
    Fixture para iniciar y detener el servidor HTTP durante las pruebas
    """
    # Crear el servidor en un puerto específico para pruebas
    server = create_server(host="localhost", port=8889)

    # Iniciar el servidor en un hilo separado
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    # Esperar un momento para que el servidor se inicie
    time.sleep(0.5)

    yield server

    # Detener el servidor después de las pruebas
    server.shutdown()
    server.server_close()
    thread.join(1)

def test_get_product_exists(server):
    """
    Prueba obtener un producto existente (ID 1)
    Debería devolver los datos del producto con código 200
    """
    response = requests.get("http://localhost:8889/product/1")
    assert response.status_code == 200, "El código de estado debe ser 200 para un producto existente."
    product = response.json()
    assert product["id"] == 1
    assert product["name"] == "Laptop"
    assert product["price"] == 999.99

def test_get_product_exists_2(server):
    """
    Prueba obtener otro producto existente (ID 2)
    Debería devolver los datos del producto con código 200
    """
    response = requests.get("http://localhost:8889/product/2")
    assert response.status_code == 200, "El código de estado debe ser 200 para un producto existente."
    product = response.json()
    assert product["id"] == 2
    assert product["name"] == "Smartphone"
    assert product["price"] == 699.99

def test_get_product_not_found(server):
    """
    Prueba obtener un producto que no existe (ID 999)
    Debería devolver un error con código 404
    """
    response = requests.get("http://localhost:8889/product/999")
    assert response.status_code == 404, "El código de estado debe ser 404 para un producto que no existe."

def test_invalid_route(server):
    """
    Prueba una ruta inválida
    Debería devolver un error con código 404
    """
    response = requests.get("http://localhost:8889/invalid")
    assert response.status_code == 404, "El código de estado debe ser 404 para rutas inválidas."
