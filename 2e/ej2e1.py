"""
Enunciado:
Desarrolla una aplicación web con Flask que demuestre diferentes formas de acceder a la
información enviada en las solicitudes HTTP. Esta aplicación te permitirá entender cómo
procesar diferentes tipos de datos proporcionados por los clientes.

Tu aplicación debe implementar los siguientes endpoints:

1. `GET /headers`: Devuelve los encabezados (headers) de la solicitud en formato JSON.
   - Muestra información como User-Agent, Accept-Language, etc.

2. `GET /browser`: Analiza el encabezado User-Agent y devuelve información sobre:
   - El navegador que está usando el cliente
   - El sistema operativo
   - Si es un dispositivo móvil o no

3. `POST /echo`: Acepta cualquier tipo de datos y devuelve exactamente los mismos datos
   en la misma forma que fueron enviados. Debe manejar:
   - JSON
   - Datos de formulario (form data)
   - Texto plano

4. `POST /validate-id`: Valida un documento de identidad según estas reglas:
   - Debe recibir un JSON con un campo "id_number"
   - El ID debe tener exactamente 9 caracteres
   - Los primeros 8 caracteres deben ser dígitos
   - El último carácter debe ser una letra
   - Devuelve JSON indicando si es válido o no

Esta actividad te enseñará cómo acceder y manipular datos de las solicitudes HTTP,
una habilidad fundamental para crear APIs robustas y aplicaciones web interactivas.
"""

from flask import Flask, jsonify, request
import re

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    @app.route('/headers', methods=['GET'])
    def get_headers():
        """
        Devuelve los encabezados (headers) de la solicitud en formato JSON.
        Convierte el objeto headers de la solicitud en un diccionario.
        """
        # Accede a los encabezados de la solicitud usando request.headers
        headers_dict = dict(request.headers)
        # Devuelve los encabezados como respuesta JSON
        return jsonify(headers_dict)

    @app.route('/browser', methods=['GET'])
    def get_browser_info():
        """
        Analiza el encabezado User-Agent y devuelve información sobre el navegador,
        sistema operativo y si es un dispositivo móvil.
        """
        user_agent = request.headers.get('User-Agent', '')

        # Detectar navegador
        if 'Chrome' in user_agent and 'Edg' not in user_agent:
            browser = 'Chrome'
        elif 'Firefox' in user_agent:
            browser = 'Firefox'
        elif 'Safari' in user_agent and 'Chrome' not in user_agent:
            browser = 'Safari'
        elif 'Edg' in user_agent:
            browser = 'Edge'
        else:
            browser = 'Desconocido'

        # Detectar sistema operativo
        if 'Windows' in user_agent:
            os = 'Windows'
        elif 'Mac OS' in user_agent:
            os = 'macOS'
        elif 'Android' in user_agent:
            os = 'Android'
        elif 'iPhone' in user_agent or 'iPad' in user_agent:
            os = 'iOS'
        else:
            os = 'Desconocido'

        # Detectar si es móvil
        is_mobile = bool(re.search(r'Mobile|Android|iPhone|iPad', user_agent))

        # Devuelve la información como respuesta JSON
        return jsonify({
            "navegador": browser,
            "sistema_operativo": os,
            "es_movil": is_mobile
        })

    @app.route('/echo', methods=['POST'])
    def echo():
        """
        Devuelve exactamente los mismos datos que recibe.
        Debe detectar el tipo de contenido y procesarlo adecuadamente.
        """
        content_type = request.content_type

        if content_type and 'application/json' in content_type:
            data = request.get_json()
            return jsonify(data)
        elif content_type and 'application/x-www-form-urlencoded' in content_type:
            data = request.form.to_dict()
            return jsonify(data)
        else:
            # Asumimos texto plano u otro tipo
            data = request.data.decode('utf-8')
            return data, 200, {'Content-Type': content_type or 'text/plain'}

    @app.route('/validate-id', methods=['POST'])
    def validate_id():
        """
        Valida un documento de identidad según reglas específicas:
        - Debe tener exactamente 9 caracteres
        - Los primeros 8 caracteres deben ser dígitos
        - El último carácter debe ser una letra
        """
        data = request.get_json()

        if not data or 'id_number' not in data:
            return jsonify({"error": "Campo 'id_number' es obligatorio"}), 400

        id_number = data['id_number']

        # Validar reglas
        if len(id_number) != 9:
            is_valid = False
        elif not id_number[:8].isdigit():
            is_valid = False
        elif not id_number[8].isalpha():
            is_valid = False
        else:
            is_valid = True

        return jsonify({
            "id_number": id_number,
            "es_valido": is_valid
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)