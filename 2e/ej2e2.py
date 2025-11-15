"""
Enunciado:
Desarrolla una aplicación web con Flask que explore los diferentes tipos MIME (Multipurpose Internet Mail Extensions)
y cómo enviar diversos formatos de contenido en respuestas HTTP. Esta aplicación te permitirá entender
cómo configurar correctamente los encabezados Content-Type para diferentes tipos de datos.

Los tipos MIME son fundamentales en el desarrollo web ya que indican al cliente (navegador, aplicación, etc.)
cómo interpretar y mostrar los datos enviados por el servidor. Una API bien diseñada debe utilizar
los tipos MIME apropiados para cada tipo de contenido.

Tu aplicación debe implementar los siguientes endpoints:

1. `GET /text`: Devuelve un texto plano con el tipo MIME `text/plain`.
   - Ejemplo de uso: Enviar mensajes simples o logs sin formato.

2. `GET /html`: Devuelve un fragmento HTML con el tipo MIME `text/html`.
   - Ejemplo de uso: Enviar contenido que debe ser renderizado como una página web.

3. `GET /json`: Devuelve un objeto JSON con el tipo MIME `application/json`.
   - Ejemplo de uso: Intercambio de datos estructurados entre cliente y servidor en APIs RESTful.

4. `GET /xml`: Devuelve un documento XML con el tipo MIME `application/xml`.
   - Ejemplo de uso: APIs SOAP, configuraciones o intercambio de datos estructurados en formato XML.

5. `GET /image`: Devuelve una imagen con el tipo MIME `image/png`.
   - Ejemplo de uso: Servir imágenes directamente desde la API.

6. `GET /binary`: Devuelve datos binarios con el tipo MIME `application/octet-stream`.
   - Ejemplo de uso: Descargar archivos como PDFs, archivos comprimidos o cualquier contenido binario genérico.

Tu tarea es completar la implementación de la función create_app() y de los endpoints solicitados,
asegurándote de utilizar el tipo MIME correcto en cada caso y generar el contenido adecuado.

Esta actividad te enseñará cómo configurar correctamente los tipos de contenido en respuestas HTTP,
una habilidad esencial para el desarrollo de APIs y servicios web que manejan diferentes formatos de datos.
"""

from flask import Flask, jsonify, Response, send_file, make_response
import os
import io

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    @app.route('/text', methods=['GET'])
    def get_text():
        """
        Devuelve un texto plano con el tipo MIME `text/plain`
        """
        response = Response("Este es un texto plano", mimetype='text/plain')
        return response

    @app.route('/html', methods=['GET'])
    def get_html():
        """
        Devuelve un fragmento HTML con el tipo MIME `text/html`
        """
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>HTML desde Flask</title>
        </head>
        <body>
            <h1>¡Hola desde Flask!</h1>
            <p>Este es un fragmento HTML.</p>
        </body>
        </html>
        """
        response = Response(html_content, mimetype='text/html')
        return response

    @app.route('/json', methods=['GET'])
    def get_json():
        """
        Devuelve un objeto JSON con el tipo MIME `application/json`
        """
        data = {"mensaje": "Hola desde JSON", "status": "ok"}
        return jsonify(data)

    @app.route('/xml', methods=['GET'])
    def get_xml():
        """
        Devuelve un documento XML con el tipo MIME `application/xml`
        """
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <mensaje>
            <titulo>XML desde Flask</titulo>
            <contenido>Este es un documento XML.</contenido>
        </mensaje>"""
        response = Response(xml_content, mimetype='application/xml')
        return response

    @app.route('/image', methods=['GET'])
    def get_image():
        """
        Devuelve una imagen con el tipo MIME `image/png`
        Para este ejemplo, crearemos una imagen PNG simple en memoria usando bytes
        """
        # Crear una imagen PNG vacía simple en bytes (esto es solo un ejemplo de bytes PNG)
        # Este es un archivo PNG vacío de 1x1 px (formato PNG)
        png_bytes = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
            b'\x00\x00\x00\nIDATx\x9cc\xf8\x0f\x00\x00\x01\x00\x01}\x0d\xcd\xcc\x80\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        buffer = io.BytesIO(png_bytes)
        response = Response(buffer.getvalue(), mimetype='image/png')
        return response

    @app.route('/binary', methods=['GET'])
    def get_binary():
        """
        Devuelve datos binarios genéricos con el tipo MIME `application/octet-stream`
        Para este ejemplo, puedes crear unos bytes aleatorios o un archivo binario simple
        """
        # Generar algunos bytes aleatorios
        binary_data = os.urandom(100)
        response = Response(binary_data, mimetype='application/octet-stream')
        return response

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
