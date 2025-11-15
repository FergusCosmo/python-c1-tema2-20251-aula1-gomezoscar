"""
Enunciado:
Desarrolla una aplicación web básica con Flask que muestre el uso del sistema de registro (logging).

En el desarrollo web es fundamental tener un buen sistema de registro de eventos,
que permita hacer seguimiento de lo que ocurre en nuestra aplicación. Flask proporciona
un objeto logger integrado (app.logger) que permite registrar mensajes con diferentes
niveles de importancia.

Tu tarea es implementar los siguientes endpoints:

1. `GET /info`: Registra un mensaje de nivel INFO y devuelve un mensaje en texto plano.
2. `GET /warning`: Registra un mensaje de nivel WARNING y devuelve un mensaje en texto plano.
3. `GET /error`: Registra un mensaje de nivel ERROR y devuelve un mensaje en texto plano.
4. `GET /critical`: Registra un mensaje de nivel CRITICAL y devuelve un mensaje en texto plano.

Esta actividad te enseñará a utilizar el sistema de registro de Flask,
una habilidad crucial para el desarrollo y depuración de aplicaciones web.
"""

from flask import Flask, request

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    # Configuración básica del logger
    # Por defecto, los mensajes se registrarán en la consola

    @app.route('/info', methods=['GET'])
    def log_info():
        """
        Registra un mensaje de nivel INFO
        """
        # Registra un mensaje de nivel INFO
        app.logger.info("Mensaje de nivel INFO registrado desde /info")
        # Devuelve un mensaje en texto plano
        return "Mensaje INFO registrado en el log"

    @app.route('/warning', methods=['GET'])
    def log_warning():
        """
        Registra un mensaje de nivel WARNING
        """
        # Registra un mensaje de nivel WARNING
        app.logger.warning("Mensaje de nivel WARNING registrado desde /warning")
        # Devuelve un mensaje en texto plano
        return "Mensaje WARNING registrado en el log"

    @app.route('/error', methods=['GET'])
    def log_error():
        """
        Registra un mensaje de nivel ERROR
        """
        # Registra un mensaje de nivel ERROR
        app.logger.error("Mensaje de nivel ERROR registrado desde /error")
        # Devuelve un mensaje en texto plano
        return "Mensaje ERROR registrado en el log"

    @app.route('/critical', methods=['GET'])
    def log_critical():
        """
        Registra un mensaje de nivel CRITICAL
        """
        # Registra un mensaje de nivel CRITICAL
        app.logger.critical("Mensaje de nivel CRITICAL registrado desde /critical")
        # Devuelve un mensaje en texto plano
        return "Mensaje CRITICAL registrado en el log"

    @app.route('/status', methods=['GET'])
    def status():
        """
        Endpoint adicional que registra diferentes mensajes según el parámetro de consulta 'level'
        Ejemplo: /status?level=warning
        """
        level = request.args.get('level', '').lower()
        message = f"Mensaje desde /status con level={level}"

        if level == 'info':
            app.logger.info(message)
        elif level == 'warning':
            app.logger.warning(message)
        elif level == 'error':
            app.logger.error(message)
        elif level == 'critical':
            app.logger.critical(message)
        else:
            return f"Nivel '{level}' no soportado. Usa: info, warning, error, critical"

        return f"Mensaje '{level.upper()}' registrado en el log"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)