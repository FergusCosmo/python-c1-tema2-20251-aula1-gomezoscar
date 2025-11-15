"""
Enunciado:
Desarrolla una aplicación web básica con Flask que responda a una petición GET y devuelva una pequeña página web.
La aplicación debe tener el siguiente endpoint:

1. `GET /greet/<nombre>`: Devuelve una página web que saluda al usuario cuyo nombre se pasa como parámetro en la URL.

Tu tarea es completar la implementación de la función create_app() y del endpoint solicitado.
Además, debes crear una plantilla HTML utilizando Jinja2 que reciba una variable `nombre` y la utilice para mostrar un mensaje de saludo.

Nota: Asegúrate de incluir una estructura HTML válida en la plantilla.
"""

from flask import Flask, render_template_string

# Implementa la plantilla HTML aquí
TEMPLATE = """
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Hola, {{ nombre }}!</title>
</head>
<body>
    <h1>¡Hola, {{ nombre }}!</h1>
    <p>Esta es una página generada dinámicamente con Flask y Jinja2.</p>
</body>
</html>
"""

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    @app.route('/greet/<nombre>', methods=['GET'])
    def greet(nombre):
        """
        Devuelve una página web que saluda al usuario utilizando una plantilla Jinja2
        """
        # Utiliza render_template_string para renderizar la plantilla con el nombre proporcionado:
        return render_template_string(TEMPLATE, nombre=nombre)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
