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
                    'mensaje': str
                }
        """
        
        system_prompt = """Eres un validador especializado en sintaxis de expresiones lógicas proposicionales. Tu tarea es evaluar si una expresión lógica está sintácticamente correcta.

        REGLAS DE SINTAXIS VÁLIDA:
        1. Las proposiciones son letras individuales (A, B, C, etc.) o palabras
        2. Los operadores válidos son: 'and', 'or', 'not' (en minúsculas)
        3. El operador 'not' es unario y debe preceder a una proposición o expresión entre paréntesis
        4. Los operadores 'and' y 'or' son binarios y requieren proposiciones/expresiones a ambos lados
        5. Los paréntesis deben estar balanceados y contener expresiones válidas
        6. No pueden haber dos operadores binarios consecutivos
        7. Una expresión no puede empezar o terminar con 'and' u 'or'

        EJEMPLOS DE EXPRESIONES VÁLIDAS:
        - "A"
        - "A or B"
        - "A and B"
        - "not A"
        - "(A or B) and C"
        - "not (A and B)"
        - "A and (B or C)"
        - "(A and B) or (C and D)"
        - "not A or B"
        - "not (not A)"

        EJEMPLOS DE EXPRESIONES INVÁLIDAS:
        - "A or and B" → Dos operadores consecutivos
        - "A or" → Operador binario sin operando derecho
        - "or A" → Operador binario sin operando izquierdo
        - "A B" → Falta operador entre proposiciones
        - "(A or B" → Paréntesis no balanceados
        - "A and and B" → Operadores duplicados
        - "not" → Operador 'not' sin operando
        - "A not B" → 'not' mal posicionado
        - "() and A" → Paréntesis vacíos
        - "A or B)" → Paréntesis no balanceados

        FORMATO DE RESPUESTA OBLIGATORIO:
        Debes responder ÚNICAMENTE con un objeto JSON válido, sin texto adicional, comentarios ni formato markdown:

        Si la expresión es válida:
        {
            "valida": true,
            "mensaje": "La expresion es correcta."
        }

        Si la expresión es inválida:
        {
            "valida": false,
            "mensaje": "[Descripción específica del error]"
        }

        MENSAJES DE ERROR ESPECÍFICOS:
        - Para operadores consecutivos: "Error de sintaxis: operadores consecutivos 'X' y 'Y' en la posición N"
        - Para paréntesis no balanceados: "Error de sintaxis: paréntesis no balanceados"
        - Para operador binario sin operando: "Error de sintaxis: el operador 'X' requiere operandos a ambos lados"
        - Para proposiciones sin operador: "Error de sintaxis: falta operador entre proposiciones"
        - Para 'not' mal usado: "Error de sintaxis: el operador 'not' debe preceder a una proposición o expresión"
        - Para paréntesis vacíos: "Error de sintaxis: paréntesis vacíos"

        IMPORTANTE:
        - Evalúa SOLO la sintaxis, NO el valor de verdad
        - Responde SOLO con el JSON, sin explicaciones adicionales
        - El mensaje de éxito debe ser SIEMPRE exactamente: "La expresion es correcta."
        - Sé específico en los mensajes de error indicando qué está mal"""
        
        
        # Crear el prompt para la API
        prompt = self._create_prompt(expression)
        
        try:
            # Preparar la solicitud
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
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
                'mensaje': f"Error al comunicarse con la API de OpenAI: {str(e)}"
            }
        except Exception as e:
            # Manejar otros errores
            return {
                'valida': False,
                'mensaje': f"Error inesperado: {str(e)}"
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
            required_keys = ['valida', 'mensaje']
            for key in required_keys:
                if key not in result:
                    return {
                        'valida': False,
                        'mensaje': f"La respuesta de la API no contiene el campo '{key}'"
                    }
            
            # Validar y convertir los tipos de datos
            result['valida'] = bool(result['valida'])
            result['mensaje'] = str(result['mensaje'])
        
        
            return result
            
        except json.JSONDecodeError:
            # Error al parsear el JSON
            return {
                'valida': False,
                'mensaje': "La respuesta de la API no es un JSON válido"
            }
        except Exception as e:
            # Otros errores
            return {
                'valida': False,
                'mensaje': f"Error al procesar la respuesta: {str(e)}"
            }
    
    def _create_prompt(self, expression):
        """
        Crea el prompt para enviar a la API de OpenAI.
        
        Args:
            expression (str): La expresión a evaluar.
            
        Returns:
            str: El prompt para la API.
        """
        
        # Crear el prompt
        prompt = f"""
Evalúa la siguiente expresión de teoría de conjuntos y determina si es sintácticamente correcta:

## Expresión a Evaluar
{expression}
"""
        
        return prompt