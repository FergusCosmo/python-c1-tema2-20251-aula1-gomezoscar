"""
Enunciado:
Desarrolla una API REST utilizando Flask que permita filtrar productos según diferentes criterios.

En APIs REST, es común necesitar obtener subconjuntos de datos basados en ciertos criterios.
Esto se implementa habitualmente mediante parámetros de consulta (query parameters) en la URL.
Por ejemplo: /products?min_price=500&category=electronics

Tu tarea es implementar el siguiente endpoint con capacidades de filtrado:

`GET /products`: Devuelve una lista de productos que se puede filtrar según diferentes criterios.
Debe admitir los siguientes parámetros de consulta:
- `category`: Filtrar productos por categoría
- `min_price`: Filtrar productos con precio igual o mayor al valor especificado
- `max_price`: Filtrar productos con precio igual o menor al valor especificado
- `name`: Filtrar productos cuyo nombre contenga la cadena especificada (búsqueda parcial)

Si no se proporciona ningún parámetro, debe devolver todos los productos.

Requisitos:
- Utiliza la lista de productos proporcionada.
- Los filtros deben poder combinarse entre sí (por ejemplo, filtrar por categoría Y precio mínimo).
- Devuelve las respuestas en formato JSON utilizando la función jsonify() de Flask.
- Asegúrate de devolver un código 200 (OK) incluso si no hay productos que cumplan los filtros.

Ejemplos:
1. `GET /products` debe devolver todos los productos.
2. `GET /products?category=electronics` debe devolver solo productos de categoría "electronics".
3. `GET /products?min_price=500&max_price=1000` debe devolver productos con precio entre 500 y 1000.
4. `GET /products?name=pro` debe devolver productos cuyo nombre contenga "pro" (como "Laptop Pro").
"""

from flask import Flask, jsonify, request

# Lista de productos predefinida con categorías
products = [
    {"id": 1, "name": "Laptop Pro", "price": 999.99, "category": "electronics"},
    {"id": 2, "name": "Smartphone X", "price": 699.99, "category": "electronics"},
    {"id": 3, "name": "Tablet Mini", "price": 349.99, "category": "electronics"},
    {"id": 4, "name": "Office Desk", "price": 249.99, "category": "furniture"},
    {"id": 5, "name": "Ergonomic Chair", "price": 189.99, "category": "furniture"},
    {"id": 6, "name": "Coffee Maker Pro", "price": 89.99, "category": "appliances"},
    {"id": 7, "name": "Wireless Headphones", "price": 129.99, "category": "electronics"},
    {"id": 8, "name": "Smart Watch", "price": 199.99, "category": "electronics"}
]

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    @app.route('/products', methods=['GET'])
    def get_products():
        """
        Devuelve una lista de productos filtrada según los parámetros de consulta.
        Parámetros admitidos:
        - category: Filtrar por categoría
        - min_price: Precio mínimo
        - max_price: Precio máximo
        - name: Buscar por nombre (coincidencia parcial)
        """
        # Obtén los parámetros de consulta
        category = request.args.get('category')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        name = request.args.get('name')

        # Convertir precios a float si están presentes
        if min_price is not None:
            try:
                min_price = float(min_price)
            except ValueError:
                return jsonify({"error": "El parámetro min_price debe ser un número válido"}), 400

        if max_price is not None:
            try:
                max_price = float(max_price)
            except ValueError:
                return jsonify({"error": "El parámetro max_price debe ser un número válido"}), 400

        # Filtrar productos según los parámetros
        filtered_products = products

        if category:
            filtered_products = [p for p in filtered_products if p["category"] == category]

        if min_price is not None:
            filtered_products = [p for p in filtered_products if p["price"] >= min_price]

        if max_price is not None:
            filtered_products = [p for p in filtered_products if p["price"] <= max_price]

        if name:
            filtered_products = [p for p in filtered_products if name.lower() in p["name"].lower()]

        return jsonify(filtered_products), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
