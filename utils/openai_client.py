"""
Módulo para manejar la conexión con la API de OpenAI.
Este módulo se encargará de enviar las expresiones de conjuntos a la API
y procesar las respuestas.
"""

import os
import json
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class OpenAIClient:
    """Cliente para interactuar con la API de OpenAI."""
    
    def __init__(self):
        """Inicializa el cliente de OpenAI con la API key del entorno."""
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("La API key de OpenAI no está configurada en las variables de entorno.")
        
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4.1-mini')
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def evaluate_expression(self, expression):
        """
        Evalúa una expresión de teoría de conjuntos utilizando la API de OpenAI.
        
        Args:
            expression (str): La expresión a evaluar (ej. "A or B").
            
        Returns:
            dict: Un diccionario con los resultados de la evaluación.
                {
                    'valida': bool,
                    'error': str o None,
                    'elementos': list,
                    'regiones': list,
                    'explicacion': str
                }
        """
        # Definir los conjuntos
        conjunto_a = {1, 4, 6, 7}
        conjunto_b = {2, 4, 5, 7}
        conjunto_c = {3, 5, 6, 7}
        
        # Crear el prompt para la API
        prompt = self._create_prompt(expression, conjunto_a, conjunto_b, conjunto_c)
        
        try:
            # Preparar la solicitud
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "Eres un asistente especializado en teoría de conjuntos."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "response_format": {"type": "json_object"}
            }
            
            # Log del prompt enviado
            print(f"[DEBUG] Prompt enviado a OpenAI:\n{prompt}\n")
            
            # Enviar la solicitud a la API
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()  # Lanzar una excepción si hay un error HTTP
            
            # Extraer la respuesta
            response_data = response.json()
            
            # Log de la respuesta cruda de OpenAI
            print(f"[DEBUG] Respuesta cruda de OpenAI:\n{json.dumps(response_data, indent=2, ensure_ascii=False)}\n")

            
            response_text = response_data["choices"][0]["message"]["content"]
            
            # Procesar la respuesta
            return self._process_response(response_text, expression)
            
        except requests.exceptions.RequestException as e:
            # Manejar errores de la API
            return {
                'valida': False,
                'error': f"Error al comunicarse con la API de OpenAI: {str(e)}",
                'elementos': [],
                'regiones': [],
                'explicacion': "Ocurrió un error al evaluar la expresión. Por favor, inténtalo de nuevo."
            }
        except Exception as e:
            # Manejar otros errores
            return {
                'valida': False,
                'error': f"Error inesperado: {str(e)}",
                'elementos': [],
                'regiones': [],
                'explicacion': "Ocurrió un error inesperado. Por favor, inténtalo de nuevo."
            }
    
    def _process_response(self, response_text, expression):
        """
        Procesa la respuesta de la API de OpenAI.
        
        Args:
            response_text (str): La respuesta de la API en formato JSON.
            expression (str): La expresión original para referencia.
            
        Returns:
            dict: Un diccionario con los resultados procesados.
        """
        try:
            # Intentar parsear la respuesta como JSON
            result = json.loads(response_text)
            
            # Verificar que la respuesta tiene la estructura esperada
            required_keys = ['valida', 'error', 'elementos', 'regiones', 'explicacion']
            for key in required_keys:
                if key not in result:
                    return {
                        'valida': False,
                        'error': f"La respuesta de la API no contiene el campo '{key}'",
                        'elementos': [],
                        'regiones': [],
                        'explicacion': "La respuesta de la API no tiene el formato esperado."
                    }
            
            # Validar y convertir los tipos de datos
            result['valida'] = bool(result['valida'])
            
            if not isinstance(result['elementos'], list):
                result['elementos'] = []
                
            if not isinstance(result['regiones'], list):
                result['regiones'] = []
            
            # Asegurarse de que los elementos son números
            result['elementos'] = [int(elem) if isinstance(elem, (int, str)) and str(elem).isdigit() else elem for elem in result['elementos']]
            
            return result
            
        except json.JSONDecodeError:
            # Error al parsear el JSON
            return {
                'valida': False,
                'error': "La respuesta de la API no es un JSON válido",
                'elementos': [],
                'regiones': [],
                'explicacion': f"No se pudo procesar la respuesta para la expresión '{expression}'."
            }
        except Exception as e:
            # Otros errores
            return {
                'valida': False,
                'error': f"Error al procesar la respuesta: {str(e)}",
                'elementos': [],
                'regiones': [],
                'explicacion': f"Ocurrió un error al procesar la respuesta para la expresión '{expression}'."
            }
    
    def _create_prompt(self, expression, conjunto_a, conjunto_b, conjunto_c):
        """
        Crea el prompt para enviar a la API de OpenAI.
        
        Args:
            expression (str): La expresión a evaluar.
            conjunto_a (set): El conjunto A.
            conjunto_b (set): El conjunto B.
            conjunto_c (set): El conjunto C.
            
        Returns:
            str: El prompt para la API.
        """
        # Convertir los conjuntos a listas ordenadas para mejor visualización
        a_list = sorted(list(conjunto_a))
        b_list = sorted(list(conjunto_b))
        c_list = sorted(list(conjunto_c))
        
        # Mapeo de regiones a elementos
        region_elements = {
            "A∩¬B∩¬C": [1],           # Solo A
            "¬A∩B∩¬C": [2],           # Solo B
            "¬A∩¬B∩C": [3],           # Solo C
            "A∩B∩¬C": [4],            # A y B, no C
            "A∩¬B∩C": [6],            # A y C, no B
            "¬A∩B∩C": [5],            # B y C, no A
            "A∩B∩C": [7]              # A, B y C
        }
        
        # Crear el prompt
        prompt = f"""
Evalúa la siguiente expresión de teoría de conjuntos y determina qué elementos y regiones de un diagrama de Venn cumplen con la expresión.

## Conjuntos Definidos
- Conjunto A: {a_list}
- Conjunto B: {b_list}
- Conjunto C: {c_list}

## Expresión a Evaluar
{expression}

## Regiones del Diagrama de Venn y sus Elementos
1. A∩¬B∩¬C (elementos que están solo en A): {region_elements["A∩¬B∩¬C"]}
2. ¬A∩B∩¬C (elementos que están solo en B): {region_elements["¬A∩B∩¬C"]}
3. ¬A∩¬B∩C (elementos que están solo en C): {region_elements["¬A∩¬B∩C"]}
4. A∩B∩¬C (elementos que están en A y B, pero no en C): {region_elements["A∩B∩¬C"]}
5. A∩¬B∩C (elementos que están en A y C, pero no en B): {region_elements["A∩¬B∩C"]}
6. ¬A∩B∩C (elementos que están en B y C, pero no en A): {region_elements["¬A∩B∩C"]}
7. A∩B∩C (elementos que están en A, B y C): {region_elements["A∩B∩C"]}

## Instrucciones
1. Analiza la expresión "{expression}" utilizando los conjuntos definidos.
2. Determina qué elementos del universo cumplen con la expresión.
3. Identifica qué regiones del diagrama de Venn deben colorearse (usa la notación exacta: "A∩¬B∩¬C", "¬A∩B∩¬C", etc.).
4. Si la expresión tiene errores de sintaxis o no es válida, proporciona un mensaje de error claro.

## Operadores Permitidos
- "and" o "∩" para la intersección
- "or" o "∪" para la unión
- "not" o "¬" para el complemento
- Paréntesis "(" y ")" para agrupar expresiones

## Formato de Respuesta
Responde ÚNICAMENTE en formato JSON con la siguiente estructura exacta:
{{
  "valida": true/false,
  "error": "Mensaje de error si la expresión no es válida, null si es válida",
  "elementos": [lista de elementos que cumplen con la expresión],
  "regiones": [lista de regiones que deben colorearse usando la notación exacta],
  "explicacion": "Breve explicación del resultado"
}}
"""
        
        return prompt