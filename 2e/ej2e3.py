"""
Enunciado:
Desarrolla una aplicación web con Flask que procese diferentes tipos MIME (Multipurpose Internet Mail Extensions)
recibidos en solicitudes HTTP. Esta aplicación te permitirá entender cómo recibir y procesar
diferentes formatos de datos enviados por los clientes.

Los tipos MIME son fundamentales en el desarrollo web ya que indican cómo interpretar los datos
recibidos en las solicitudes HTTP. Una API robusta debe poder manejar diversos formatos de entrada.

Tu aplicación debe implementar los siguientes endpoints:

1. `POST /text`: Recibe un texto plano con el tipo MIME `text/plain` y lo devuelve en la respuesta.
   - Ejemplo de uso: Procesar mensajes simples o logs enviados por el cliente.

2. `POST /html`: Recibe un fragmento HTML con el tipo MIME `text/html` y lo devuelve en la respuesta.
   - Ejemplo de uso: Recibir contenido HTML para almacenar o procesar.

3. `POST /json`: Recibe un objeto JSON con el tipo MIME `application/json` y lo devuelve en la respuesta.
   - Ejemplo de uso: Procesar datos estructurados en APIs RESTful.

4. `POST /xml`: Recibe un documento XML con el tipo MIME `application/xml` y lo devuelve en la respuesta.
   - Ejemplo de uso: Procesar configuraciones o datos estructurados en formato XML.

5. `POST /image`: Recibe una imagen con el tipo MIME `image/png` o `image/jpeg` y la guarda en el servidor.
   - Ejemplo de uso: Subir imágenes para un perfil de usuario o una galería.

6. `POST /binary`: Recibe datos binarios con el tipo MIME `application/octet-stream` y confirma su recepción.
   - Ejemplo de uso: Recibir archivos genéricos como PDFs o archivos comprimidos.

Tu tarea es completar la implementación de la función create_app() y de los endpoints solicitados,
asegurándote de identificar correctamente el tipo MIME de cada solicitud y procesarla adecuadamente.

Esta actividad te enseñará cómo recibir y manejar diferentes tipos de datos en solicitudes HTTP,
una habilidad esencial para desarrollar APIs web que interactúan con diversos clientes.
"""

from flask import Flask, jsonify, request, Response
import os
import uuid

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    # Crear un directorio para guardar archivos subidos si no existe
    uploads_dir = os.path.join(app.instance_path, 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)

    @app.route('/text', methods=['POST'])
    def post_text():
        """
        Recibe un texto plano con el tipo MIME `text/plain` y lo devuelve en la respuesta.
        """
        # Verifica que el Content-Type sea text/plain
        if request.content_type != 'text/plain':
            return jsonify({"error": "Tipo de contenido incorrecto, se esperaba text/plain"}), 400

        # Lee el contenido de la solicitud
        text_content = request.data.decode('utf-8')

        # Devuelve el mismo texto con Content-Type text/plain
        return Response(text_content, mimetype='text/plain')

    @app.route('/html', methods=['POST'])
    def post_html():
        """
        Recibe un fragmento HTML con el tipo MIME `text/html` y lo devuelve en la respuesta.
        """
        # Verifica que el Content-Type sea text/html
        if request.content_type != 'text/html':
            return jsonify({"error": "Tipo de contenido incorrecto, se esperaba text/html"}), 400

        # Lee el contenido de la solicitud
        html_content = request.data.decode('utf-8')

        # Devuelve el mismo HTML con Content-Type text/html
        return Response(html_content, mimetype='text/html')

    @app.route('/json', methods=['POST'])
    def post_json():
        """
        Recibe un objeto JSON con el tipo MIME `application/json` y lo devuelve en la respuesta.
        """
        # Accede al contenido JSON usando request.get_json()
        json_data = request.get_json()

        if json_data is None:
            return jsonify({"error": "No se recibió un JSON válido"}), 400

        # Devuelve el mismo objeto JSON usando jsonify()
        return jsonify(json_data)

    @app.route('/xml', methods=['POST'])
    def post_xml():
        """
        Recibe un documento XML con el tipo MIME `application/xml` y lo devuelve en la respuesta.
        """
        # Verifica que el Content-Type sea application/xml
        if not request.content_type or 'application/xml' not in request.content_type:
            return jsonify({"error": "Tipo de contenido incorrecto, se esperaba application/xml"}), 400

        # Lee el contenido XML de la solicitud
        xml_content = request.data.decode('utf-8')

        # Devuelve el mismo XML con Content-Type application/xml
        return Response(xml_content, mimetype='application/xml')

    @app.route('/image', methods=['POST'])
    def post_image():
        """
        Recibe una imagen con el tipo MIME `image/png` o `image/jpeg` y la guarda en el servidor.
        """
        # Verifica que el Content-Type sea image/png o image/jpeg
        content_type = request.content_type
        if content_type not in ['image/png', 'image/jpeg']:
            return jsonify({"error": "Tipo de imagen no soportado. Solo se aceptan PNG o JPEG."}), 400

        # Lee los datos binarios de la imagen
        image_data = request.data

        # Genera un nombre único para el archivo
        filename = f"{uuid.uuid4().hex}.png" if content_type == 'image/png' else f"{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(uploads_dir, filename)

        # Guarda la imagen en el directorio 'uploads'
        with open(filepath, 'wb') as f:
            f.write(image_data)

        # Devuelve una confirmación con el nombre del archivo guardado
        return jsonify({
            "mensaje": "Imagen guardada exitosamente",
            "archivo": filename
        })

    @app.route('/binary', methods=['POST'])
    def post_binary():
        """
        Recibe datos binarios con el tipo MIME `application/octet-stream` y confirma su recepción.
        """
        # Verifica que el Content-Type sea application/octet-stream
        if request.content_type != 'application/octet-stream':
            return jsonify({"error": "Tipo de contenido incorrecto, se esperaba application/octet-stream"}), 400

        # Lee los datos binarios de la solicitud
        binary_data = request.data

        # Genera un nombre único para el archivo
        filename = f"{uuid.uuid4().hex}.bin"
        filepath = os.path.join(uploads_dir, filename)

        # Guarda los datos binarios
        with open(filepath, 'wb') as f:
            f.write(binary_data)

        # Devuelve una confirmación con información sobre los datos recibidos
        return jsonify({
            "mensaje": "Datos binarios recibidos y guardados exitosamente",
            "archivo": filename,
            "tamaño_bytes": len(binary_data)
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
