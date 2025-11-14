"""
Enunciado:
Desarrolla una API REST básica utilizando la biblioteca http.server de Python con un endpoint que devuelve información sobre productos en formato XML.

Tu tarea es implementar el siguiente endpoint:

`GET /product/<id>`: Devuelve información sobre un producto específico por su ID.
- Si el producto existe, devuelve los datos del producto en formato XML con código 200 (OK).
- Si el producto no existe, devuelve un mensaje de error con código 404 (Not Found).

Requisitos:
- Utiliza la lista de productos proporcionada.
- Devuelve las respuestas en formato XML.
- Asegúrate de utilizar los códigos de estado HTTP apropiados.

Ejemplo:
1. Una solicitud `GET /product/1` debe devolver los datos del producto con ID 1 en formato XML y código 200.
2. Una solicitud `GET /product/999` debe devolver un mensaje de error con código 404.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Lista de productos predefinida
products = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Smartphone", "price": 699.99},
    {"id": 3, "name": "Tablet", "price": 349.99}
]

def dict_to_xml(tag, d):
    """
    Convierte un diccionario en un elemento XML
    """
    elem = ET.Element(tag)
    for key, val in d.items():
        child = ET.SubElement(elem, key)
        child.text = str(val)
    return elem

def prettify(elem):
    """
    Devuelve una cadena XML formateada bonita
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ").encode()

class ProductAPIHandler(BaseHTTPRequestHandler):
    """
    Manejador de peticiones HTTP para la API de productos en XML
    """

    def do_GET(self):
        """
        Método que se ejecuta cuando se recibe una petición GET.
        Debes implementar la lógica para responder a la petición GET en la ruta /product/<id>
        con los datos del producto en formato XML si existe, o un error 404 si no existe.
        """
        # Usa una expresión regular para verificar si la ruta coincide con /product/<id>
        match = re.match(r'^/product/(\d+)$', self.path)
        
        if match:
            # Extrae el ID del producto de la ruta
            product_id = int(match.group(1))
            
            # Busca el producto en la lista
            product = None
            for p in products:
                if p["id"] == product_id:
                    product = p
                    break
            
            if product:
                # Si el producto existe, convierte el producto a XML
                product_xml = dict_to_xml("product", product)
                xml_response = prettify(product_xml)
                
                # Devuelve el XML con código 200
                self.send_response(200)
                self.send_header("Content-Type", "application/xml; charset=utf-8")
                self.end_headers()
                self.wfile.write(xml_response)
            else:
                # Si el producto no existe, devuelve un mensaje de error XML con código 404
                error_dict = {
                    "error": "Producto no encontrado",
                    "id": product_id
                }
                error_xml = dict_to_xml("error_response", error_dict)
                xml_response = prettify(error_xml)
                
                self.send_response(404)
                self.send_header("Content-Type", "application/xml; charset=utf-8")
                self.end_headers()
                self.wfile.write(xml_response)
        else:
            # Si la ruta no coincide con el patrón esperado, devuelve 404
            error_dict = {
                "error": "Ruta no encontrada",
                "path": self.path
            }
            error_xml = dict_to_xml("error_response", error_dict)
            xml_response = prettify(error_xml)
            
            self.send_response(404)
            self.send_header("Content-Type", "application/xml; charset=utf-8")
            self.end_headers()
            self.wfile.write(xml_response)

def create_server(host="localhost", port=8000):
    """
    Crea y configura el servidor HTTP
    """
    server_address = (host, port)
    httpd = HTTPServer(server_address, ProductAPIHandler)
    return httpd

def run_server(server):
    """
    Inicia el servidor HTTP
    """
    print(f"Servidor iniciado en http://{server.server_name}:{server.server_port}")
    server.serve_forever()

if __name__ == '__main__':
    server = create_server()
    run_server(server)  