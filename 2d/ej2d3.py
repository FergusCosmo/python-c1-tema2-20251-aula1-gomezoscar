"""
Enunciado:
Desarrolla una API REST utilizando Flask que gestione un catálogo de animales e implemente
manejo de errores personalizado con el decorador @app.errorhandler.

La API debe exponer los siguientes endpoints:

1. `GET /animals`: Devuelve la lista completa de animales.
2. `GET /animals/<animal_id>`: Devuelve la información de un animal específico por su ID.
3. `POST /animals`: Agrega un nuevo animal. El cuerpo debe incluir JSON con campos "name" y "species".
4. `DELETE /animals/<animal_id>`: Elimina un animal específico por su ID.

Además, debes implementar manejadores personalizados para los siguientes errores HTTP:

- 400 (Bad Request): Cuando faltan datos necesarios o tienen formato incorrecto.
- 404 (Not Found): Cuando se solicita un animal que no existe.
- 405 (Method Not Allowed): Cuando se utiliza un método HTTP no permitido.
- 500 (Internal Server Error): Para errores internos del servidor.

Requisitos:
- Implementar los manejadores de errores utilizando el decorador @app.errorhandler.
- Cada manejador debe devolver una respuesta JSON con un mensaje descriptivo y el código de estado correspondiente.
- Asegúrate de que la función delete_animal lance un error 404 cuando se intenta eliminar un animal que no existe.
- Implementa un manejador para el error 500 que registre el error en los logs de la aplicación.

Ejemplo:
- Una solicitud a un endpoint inexistente debe activar el manejador de error 404.
- Una solicitud POST sin los campos requeridos debe activar el manejador de error 400.
- Intentar eliminar un animal inexistente debe activar el manejador de error 404.

Tu tarea es implementar esta API en Flask con el manejo adecuado de errores.
"""

from flask import Flask, jsonify, request, abort
import logging

# Configuración del registro (logging)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lista de animales predefinida
animals = [
    {"id": 1, "name": "León", "species": "Panthera leo"},
    {"id": 2, "name": "Elefante", "species": "Loxodonta africana"},
    {"id": 3, "name": "Jirafa", "species": "Giraffa camelopardalis"}
]

# Este contador se usará para asignar IDs únicos
next_id = 4

def create_app():
    """
    Crea y configura la aplicación Flask con manejadores de errores personalizados
    """
    app = Flask(__name__)
    
    # Manejador de errores 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(error):
        """
        Maneja errores de solicitud incorrecta (400)
        Devuelve un JSON con mensaje de error y código de estado 400
        """
        # Registra el error usando app.logger.warning() con un mensaje descriptivo
        app.logger.warning(f"Error 400: Solicitud incorrecta en {request.path}")
        # Devuelve un JSON con un mensaje descriptivo y el código de estado 400
        return jsonify({
            "error": "Solicitud incorrecta",
            "message": "Faltan datos o formato incorrecto"
        }), 400

    # Manejador de errores 404 - Not Found
    @app.errorhandler(404)
    def not_found(error):
        """
        Maneja errores de recurso no encontrado (404)
        Devuelve un JSON con mensaje de error y código de estado 404
        """
        # Registra el error usando app.logger.info() con un mensaje descriptivo
        app.logger.info(f"Error 404: Recurso no encontrado en {request.path}")
        # Devuelve un JSON con un mensaje descriptivo y el código de estado 404
        return jsonify({
            "error": "Recurso no encontrado",
            "message": "El animal solicitado no existe"
        }), 404

    # Manejador de errores 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(error):
        """
        Maneja errores de método no permitido (405)
        Devuelve un JSON con mensaje de error y código de estado 405
        """
        # Registra el error usando app.logger.warning() con un mensaje descriptivo
        app.logger.warning(f"Error 405: Método no permitido en {request.path}")
        # Devuelve un JSON con un mensaje descriptivo y el código de estado 405
        return jsonify({
            "error": "Método no permitido",
            "message": f"El método {request.method} no está permitido para esta ruta"
        }), 405

    # Manejador de errores 500 - Internal Server Error
    @app.errorhandler(500)
    def internal_error(error):
        """
        Maneja errores internos del servidor (500)
        Registra el error en los logs y devuelve un JSON con mensaje de error
        """
        # Registra el error usando app.logger.error() con los detalles del error
        app.logger.error(f"Error 500: Error interno del servidor en {request.path} - {str(error)}")
        # Devuelve un JSON con un mensaje descriptivo y el código de estado 500
        return jsonify({
            "error": "Error interno del servidor",
            "message": "Ocurrió un error inesperado en el servidor"
        }), 500

    @app.route('/animals', methods=['GET'])
    def get_animals():
        """
        Devuelve la lista completa de animales
        """
        # Devuelve la lista de animales en formato JSON con código 200
        return jsonify(animals), 200

    @app.route('/animals/<int:animal_id>', methods=['GET'])
    def get_animal(animal_id):
        """
        Devuelve la información de un animal específico por su ID
        Si el animal no existe, debe activar un error 404
        """
        animal = next((a for a in animals if a['id'] == animal_id), None)
        if animal is None:
            # Si el animal no existe, usa abort(404) para lanzar un error 404
            abort(404)
        return jsonify(animal), 200

    @app.route('/animals', methods=['POST'])
    def add_animal():
        """
        Agrega un nuevo animal
        El cuerpo debe incluir JSON con campos "name" y "species"
        Si falta algún campo, debe activar un error 400
        """
        # Verifica que el cuerpo de la solicitud contenga JSON
        data = request.get_json()
        if not data or 'name' not in data or 'species' not in data:
            # Si falta algún campo, usa abort(400) para lanzar un error
            abort(400)

        # Si todo está correcto, agrega el nuevo animal a la lista y devuelve una respuesta adecuada (código 201)
        global next_id
        new_animal = {
            "id": next_id,
            "name": data["name"],
            "species": data["species"]
        }
        animals.append(new_animal)
        next_id += 1
        return jsonify(new_animal), 201

    @app.route('/animals/<int:animal_id>', methods=['DELETE'])
    def delete_animal(animal_id):
        """
        Elimina un animal específico por su ID
        Si el animal no existe, debe activar un error 404
        """
        # Verifica si el animal existe
        animal = next((a for a in animals if a["id"] == animal_id), None)

        if not animal:
            # Si no existe, usa abort(404) para lanzar un error 404
            abort(404)

        # Si existe, elimínalo de la lista y devuelve una respuesta adecuada
        global animals
        animals = [a for a in animals if a["id"] != animal_id]
        return jsonify({"message": "Animal eliminado", "id": animal_id}), 200

    # Endpoint adicional que lanza un error 500 para probar el manejador
    @app.route('/test-error', methods=['GET'])
    def test_error():
        """
        Endpoint de prueba que lanza un error 500 intencionalmente
        """
        # Lanza una excepción para probar el manejador de error 500
        raise Exception("¡Este es un error de prueba!")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)