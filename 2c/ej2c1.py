"""
Enunciado:
Desarrolla una API REST básica utilizando Flask con un endpoint que devuelve información sobre productos.

En las actividades anteriores, implementaste una API utilizando la biblioteca http.server de Python,
lo que requería escribir código para manejar rutas, analizar parámetros, establecer cabeceras HTTP y
serializar las respuestas manualmente. Ahora veremos cómo Flask simplifica enormemente este proceso.

Flask ofrece varias ventajas:
- Gestión automática de rutas y parámetros URL
- Conversión automática entre Python y JSON mediante jsonify()
- Manejo simplificado de códigos de estado HTTP
- No necesitas preocuparte por configurar manualmente cabeceras Content-Type

Tu tarea es implementar el siguiente endpoint:

`GET /product/<id>`: Devuelve información sobre un producto específico por su ID.
- Si el producto existe, devuelve los datos del producto con código 200 (OK).
- Si el producto no existe, devuelve un mensaje de error con código 404 (Not Found).

Requisitos:
- Utiliza la lista de productos proporcionada.
- Devuelve las respuestas en formato JSON utilizando la función jsonify() de Flask.
- Asegúrate de utilizar los códigos de estado HTTP apropiados.

Ejemplo:
1. Una solicitud `GET /product/1` debe devolver los datos del producto con ID 1 y código 200.
2. Una solicitud `GET /product/999` debe devolver un mensaje de error con código 404.
"""

from flask import Flask, jsonify

# Lista de productos predefinida
products = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Smartphone", "price": 699.99},
    {"id": 3, "name": "Tablet", "price": 349.99}
]

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    @app.route('/product/<int:product_id>', methods=['GET'])
    def get_product(product_id):
        """
        Devuelve información sobre un producto específico por su ID
        - Si existe: devuelve el producto con código 200 (OK)
        - Si no existe: devuelve un error con código 404 (Not Found)
        """
        # Busca el producto en la lista
        product = next((p for p in products if p["id"] == product_id), None)

        if product:
            # Si el producto existe, devuelve los datos con código 200
            return jsonify(product), 200
        else:
            # Si no existe, devuelve un mensaje de error con código 404
            return jsonify({"error": "Producto no encontrado", "id": product_id}), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)