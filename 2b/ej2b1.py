"""
Enunciado:
Desarrolla una aplicación web básica con Flask que responda a una petición GET.
La aplicación debe tener un único endpoint:

1. `GET /`: Devuelve un mensaje de saludo en texto plano con el contenido "¡Hola mundo!".

Esta es una introducción simple a Flask para entender cómo crear una aplicación web básica y responder
a solicitudes HTTP.

Tu tarea es completar la implementación de la función create_app() y del endpoint solicitado.

Nota: Si deseas cambiar el idioma del ejercicio, edita el archivo de test correspondiente (ej1a1_test.py).
"""

from flask import Flask

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def index():  # type: ignore
        """
        Endpoint raíz que devuelve un mensaje de saludo
        """
        return "¡Hola mundo!", 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 