"""
Enunciado:
Desarrolla una aplicación web con Flask que utilice la función abort() para devolver
diferentes códigos de estado HTTP según ciertas condiciones.

La función abort() de Flask permite terminar prematuramente una solicitud con un código
de estado HTTP específico. Esto es útil para indicar errores como recurso no encontrado (404),
acceso prohibido (403), etc.

Tu tarea es implementar los siguientes endpoints:

1. `GET /resource/<id>`: Debe devolver un mensaje con el ID solicitado si el ID es un número positivo.
   Si el ID es 0 o negativo, debe abortar la solicitud con código 400 (Bad Request).
   Si el ID es mayor que 100, debe abortar la solicitud con código 404 (Not Found).

2. `GET /admin`: Debe verificar si existe un parámetro de consulta 'key'.
   Si 'key' no está presente, debe abortar la solicitud con código 401 (Unauthorized).
   Si 'key' no es igual a 'secret123', debe abortar la solicitud con código 403 (Forbidden).

Esta actividad te enseñará a utilizar la función abort() de Flask para manejar
situaciones de error comunes en aplicaciones web.
"""

from flask import Flask, request, abort

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    @app.route('/resource/<int:resource_id>', methods=['GET'])
    def get_resource(resource_id):
        """
        Devuelve información sobre un recurso según su ID.
        Utiliza abort() en casos de error:
        - Si el ID es <= 0: abort con código 400 (Bad Request)
        - Si el ID es > 100: abort con código 404 (Not Found)
        """
        if resource_id <= 0:
            abort(400)  # Bad Request
        if resource_id > 100:
            abort(404)  # Not Found

        # Si no se cumple ninguna condición de error, devuelve el recurso
        return f"Recurso con ID {resource_id}"

    @app.route('/admin', methods=['GET'])
    def admin():
        """
        Endpoint protegido que requiere una clave de acceso.
        Utiliza abort() en casos de error:
        - Si no se proporciona el parámetro 'key': abort con código 401 (Unauthorized)
        - Si la clave no es 'secret123': abort con código 403 (Forbidden)
        """
        key = request.args.get('key')

        if not key:
            abort(401)  # Unauthorized

        if key != 'secret123':
            abort(403)  # Forbidden

        # Si no se cumple ninguna condición de error, devuelve acceso permitido
        return "Acceso concedido al panel de administración"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)