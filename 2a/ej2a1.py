"""
Enunciado:
Desarrolla un servidor web básico utilizando la biblioteca http.server de Python.
El servidor debe responder a una petición GET en la ruta raíz.

1. GET /: Devuelve un mensaje de saludo en texto plano con el contenido "¡Hola mundo!".

Esta es una introducción simple a los servidores HTTP en Python para entender cómo crear
una aplicación web básica sin usar frameworks y responder a solicitudes HTTP.

Tu tarea es completar la implementación de la clase MyHTTPRequestHandler.

Nota: Si deseas cambiar el idioma del ejercicio, edita el archivo de test correspondiente (ej2a1_test.py).
"""

from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Manejador de peticiones HTTP personalizado
    """

    def do_GET(self):
        """
        Método que se ejecuta cuando se recibe una petición GET.
        Debes implementar la lógica para responder a la petición GET en la ruta raíz ("/")
        con el mensaje "¡Hola mundo!" en texto plano.

        Para otras rutas, devuelve un código de estado 404 (Not Found).
        """
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write("¡Hola mundo!".encode())
        else:
            self.send_response(404)
            self.end_headers()


def create_server(host="localhost", port=8000):
    """
    Crea y configura el servidor HTTP
    """
    server_address = (host, port)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
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
