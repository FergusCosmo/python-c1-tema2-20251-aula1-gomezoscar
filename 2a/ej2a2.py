"""
Enunciado:
Desarrolla una API REST básica utilizando la biblioteca http.server de Python con un endpoint que devuelve información sobre productos.

Tu tarea es implementar el siguiente endpoint:

`GET /product/<id>`: Devuelve información sobre un producto específico por su ID.
- Si el producto existe, devuelve los datos del producto con código 200 (OK).
- Si el producto no existe, devuelve un mensaje de error con código 404 (Not Found).

Requisitos:
- Utiliza la lista de productos proporcionada.
- Devuelve las respuestas en formato JSON.
- Asegúrate de utilizar los códigos de estado HTTP apropiados.

Ejemplo:
1. Una solicitud `GET /product/1` debe devolver los datos del producto con ID 1 y código 200.
2. Una solicitud `GET /product/999` debe devolver un mensaje de error con código 404.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import re

# Lista de productos predefinida
products = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Smartphone", "price": 699.99},
    {"id": 3, "name": "Tablet", "price": 349.99}
]

class ProductAPIHandler(BaseHTTPRequestHandler):
    """
    Manejador de peticiones HTTP para la API de productos
    """

    def do_GET(self):
        """
        Método que se ejecuta cuando se recibe una petición GET.
        Debes implementar la lógica para responder a la petición GET en la ruta /product/<id>
        con los datos del producto en formato JSON si existe, o un error 404 si no existe.
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
                # Si el producto existe, devuélvelo en formato JSON con código 200
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                
                # Convierte el producto a JSON y envíalo
                response = json.dumps(product, ensure_ascii=False)
                self.wfile.write(response.encode("utf-8"))
            else:
                # Si el producto no existe, devuelve un mensaje de error con código 404
                self.send_response(404)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                
                error_message = {
                    "error": "Producto no encontrado",
                    "id": product_id
                }
                response = json.dumps(error_message, ensure_ascii=False)
                self.wfile.write(response.encode("utf-8"))
        else:
            # Si la ruta no coincide con el patrón esperado, devuelve 404
            self.send_response(404)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            
            error_message = {
                "error": "Ruta no encontrada",
                "path": self.path
            }
            response = json.dumps(error_message, ensure_ascii=False)
            self.wfile.write(response.encode("utf-8"))

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
