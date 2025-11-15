"""
Enunciado:
Desarrolla una aplicación web con Flask que utilice Blueprints para organizar las rutas.
Los Blueprints son una característica de Flask que permite organizar una aplicación en componentes modulares y reutilizables.

Tu tarea es implementar una aplicación con dos blueprints:

1. Blueprint 'main': Para las rutas principales
   - `GET /`: Devuelve un mensaje de bienvenida en texto plano.
   - `GET /about`: Devuelve información sobre la aplicación en texto plano.

2. Blueprint 'user': Para las rutas relacionadas con usuarios
   - `GET /user/profile/<username>`: Devuelve un perfil de usuario personalizado en texto plano.
   - `GET /user/list`: Devuelve una lista de usuarios de ejemplo en texto plano.

Además, debes:
   - Registrar ambos blueprints en la aplicación principal
   - Configurar un prefijo URL '/api/v1' para todas las rutas

Esta estructura refleja cómo se organizan las aplicaciones Flask más grandes y complejas,
separando la lógica en componentes modulares que pueden desarrollarse y mantenerse de manera independiente.
"""

from flask import Flask, Blueprint

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    # Crea el blueprint 'main'
    main_blueprint = Blueprint('main', __name__)

    # Define las rutas para el blueprint 'main'
    @main_blueprint.route('/')
    def home():
        return "¡Bienvenido a la aplicación!"

    @main_blueprint.route('/about')
    def about():
        return "Esta es una aplicación Flask que utiliza Blueprints para organizar rutas."

    # Crea el blueprint 'user'
    user_blueprint = Blueprint('user', __name__)

    # Define las rutas para el blueprint 'user'
    @user_blueprint.route('/profile/<username>')
    def user_profile(username):
        return f"Perfil de usuario: {username}"

    @user_blueprint.route('/list')
    def user_list():
        users = ["Juan", "Ana", "Pedro", "María"]
        return f"Lista de usuarios: {', '.join(users)}"

    # Registra los blueprints con un prefijo de URL '/api/v1'
    # Usa app.register_blueprint() con el parámetro url_prefix
    app.register_blueprint(main_blueprint, url_prefix='/api/v1')
    app.register_blueprint(user_blueprint, url_prefix='/api/v1')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
