from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from utils.openai_client import OpenAIClient
from utils.venn_diagram import VennDiagram

# Cargar variables de entorno
load_dotenv()

# Inicializar la aplicación Flask
app = Flask(__name__)

# Definir los conjuntos fijos
CONJUNTO_A = {1, 4, 6, 7}
CONJUNTO_B = {2, 4, 5, 7}
CONJUNTO_C = {3, 5, 6, 7}

# Inicializar el cliente de OpenAI y el generador de diagramas
openai_client = OpenAIClient()
venn_diagram = VennDiagram()

@app.route('/')
def index():
    """Ruta principal que renderiza la página de inicio."""
    return render_template('index.html')

@app.route('/health')
def health():
    """Ruta para verificar que la aplicación está funcionando."""
    return jsonify({"status": "ok", "message": "La aplicación está funcionando correctamente"})

@app.route('/api/evaluate', methods=['POST'])
def evaluate_expression():
    """
    Ruta para evaluar expresiones de teoría de conjuntos.
    
    Recibe una expresión del usuario, la evalúa utilizando la API de OpenAI,
    y devuelve el resultado en formato JSON.
    """
    # Obtener la expresión del cuerpo de la solicitud
    data = request.get_json()
    
    if not data or 'expression' not in data:
        return jsonify({
            'success': False,
            'error': 'Se requiere una expresión para evaluar',
            'elementos': [],
            'regiones': [],
            'explicacion': 'No se proporcionó una expresión para evaluar'
        }), 400
    
    expression = data['expression'].strip()
    
    if not expression:
        return jsonify({
            'success': False,
            'error': 'La expresión no puede estar vacía',
            'elementos': [],
            'regiones': [],
            'explicacion': 'Por favor, proporciona una expresión no vacía'
        }), 400
    
    try:
        # Evaluar la expresión utilizando el cliente de OpenAI
        result = openai_client.evaluate_expression(expression)
        
        # Generar el SVG del diagrama de Venn
        svg = venn_diagram.generate_svg(result.get('regiones', []), result.get('elementos', []))
        
        # Añadir el SVG al resultado
        result['svg'] = svg
        
        # Convertir 'valida' a 'success' para mantener consistencia en la API
        result['success'] = result.pop('valida', False)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al evaluar la expresión: {str(e)}',
            'elementos': [],
            'regiones': [],
            'explicacion': 'Ocurrió un error al procesar la solicitud',
            'svg': venn_diagram.generate_svg([], [])
        }), 500

if __name__ == '__main__':
    # Obtener el puerto del entorno o usar 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    # Ejecutar la aplicación en modo debug durante el desarrollo
    app.run(host='0.0.0.0', port=port, debug=True)