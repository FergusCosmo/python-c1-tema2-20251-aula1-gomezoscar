import pytest
import threading
import requests
import time
import xml.etree.ElementTree as ET
from ej2a3 import create_server

@pytest.fixture
def server():
    """
    Fixture para iniciar y detener el servidor HTTP durante las pruebas
    """
    # Crear el servidor en un puerto específico para pruebas
    server = create_server(host="localhost", port=8890)

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
    Debería devolver los datos del producto en XML con código 200
    """
    response = requests.get("http://localhost:8890/product/1")
    assert response.status_code == 200, "El código de estado debe ser 200 para un producto existente."
    assert response.headers['Content-Type'] == "application/xml", "El Content-Type debe ser application/xml"

    # Parsear la respuesta XML
    root = ET.fromstring(response.content)

    # Verificar los valores del producto
    assert root.tag == "product", "El elemento raíz debe ser 'product'"
    assert root.find("id").text == "1"
    assert root.find("name").text == "Laptop"
    assert root.find("price").text == "999.99"

def test_get_product_exists_2(server):
    """
    Prueba obtener otro producto existente (ID 2)
    Debería devolver los datos del producto en XML con código 200
    """
    response = requests.get("http://localhost:8890/product/2")
    assert response.status_code == 200, "El código de estado debe ser 200 para un producto existente."
    assert response.headers['Content-Type'] == "application/xml", "El Content-Type debe ser application/xml"

    # Parsear la respuesta XML
    root = ET.fromstring(response.content)

    # Verificar los valores del producto
    assert root.tag == "product", "El elemento raíz debe ser 'product'"
    assert root.find("id").text == "2"
    assert root.find("name").text == "Smartphone"
    assert root.find("price").text == "699.99"

def test_get_product_not_found(server):
    """
    Prueba obtener un producto que no existe (ID 999)
    Debería devolver un mensaje de error XML con código 404
    """
    response = requests.get("http://localhost:8890/product/999")
    assert response.status_code == 404, "El código de estado debe ser 404 para un producto que no existe."
    assert response.headers['Content-Type'] == "application/xml", "El Content-Type debe ser application/xml"

    # Verificar que sea un XML de error
    assert "<error>" in response.text, "El XML debe contener un elemento 'error'"

def test_invalid_route(server):
    """
    Prueba una ruta inválida
    Debería devolver un mensaje de error XML con código 404
    """
    response = requests.get("http://localhost:8890/invalid")
    assert response.status_code == 404, "El código de estado debe ser 404 para rutas inválidas."
    assert response.headers['Content-Type'] == "application/xml", "El Content-Type debe ser application/xml"

    # Verificar que sea un XML de error
    assert "<error>" in response.text, "El XML debe contener un elemento 'error'"
