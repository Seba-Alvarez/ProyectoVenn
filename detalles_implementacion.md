# Detalles de Implementación - Proyecto Venn

## Descripción de los Hitos

### HITO 1: Configuración inicial del proyecto

Este hito establece la base del proyecto. Crearemos la estructura de directorios y configuraremos el entorno de desarrollo.

**Detalles técnicos:**
- Utilizaremos Flask como framework web
- Dependencias iniciales: Flask, requests, python-dotenv, openai
- El archivo .env contendrá la clave de API de OpenAI (OPENAI_API_KEY)

### HITO 2: Implementación de la interfaz básica

En este hito, crearemos una interfaz web simple con un formulario para ingresar expresiones y un área para mostrar el diagrama.

**Detalles técnicos:**
- Utilizaremos Jinja2 (incluido en Flask) para las plantillas HTML
- La interfaz inicial será minimalista: un campo de texto, un botón y un área para el diagrama
- La ruta inicial solo renderizará la plantilla con un mensaje de "Hola Mundo"

### HITO 3: Integración con la API de OpenAI

Este hito implementa la conexión con la API de OpenAI para evaluar las expresiones de conjuntos.

**Detalles técnicos:**
- Utilizaremos la biblioteca oficial de OpenAI para Python
- El prompt para la IA incluirá:
  - Definición de los conjuntos A, B y C
  - La expresión a evaluar
  - Instrucciones para calcular los subconjuntos que cumplen con la expresión
  - Formato esperado de la respuesta (JSON)
- Ejemplo de prompt:
  ```
  Evalúa la siguiente expresión de teoría de conjuntos:
  
  Conjuntos:
  A = {1, 4, 6, 7}
  B = {2, 4, 5, 7}
  C = {3, 5, 6, 7}
  
  Expresión: A or B
  
  Calcula qué elementos cumplen con esta expresión y determina qué regiones del diagrama de Venn deben colorearse.
  
  Responde en formato JSON con:
  1. Los elementos que cumplen la expresión
  2. Las regiones que deben colorearse (usando la notación: A∩B∩C, A∩B∩¬C, etc.)
  3. Si hay algún error en la expresión
  ```

### HITO 4: Implementación del generador de diagramas de Venn

En este hito, crearemos la lógica para generar y visualizar diagramas de Venn basados en las expresiones evaluadas.

**Detalles técnicos:**
- Utilizaremos SVG para crear los diagramas de Venn
- Las regiones del diagrama se definirán con coordenadas específicas
- Cada región tendrá un ID único que corresponde a su definición matemática
- Mapeo de regiones:
  1. A∩¬B∩¬C (solo A)
  2. ¬A∩B∩¬C (solo B)
  3. ¬A∩¬B∩C (solo C)
  4. A∩B∩¬C (A y B)
  5. A∩¬B∩C (A y C)
  6. ¬A∩B∩C (B y C)
  7. A∩B∩C (A, B y C)

### HITO 5: Pruebas y refinamiento

Este hito se enfoca en probar la aplicación con diferentes expresiones y mejorar la experiencia del usuario.

**Detalles técnicos:**
- Probaremos expresiones simples: "A", "B", "C", "A or B", "A and B"
- Probaremos expresiones complejas: "A and (B or C)", "(A or B) and not C"
- Implementaremos mensajes de error claros para expresiones inválidas
- Mejoraremos la visualización del diagrama según los resultados de las pruebas

### HITO 6: Despliegue

Este hito prepara la aplicación para su despliegue en un entorno de producción.

**Detalles técnicos:**
- Configuraremos Gunicorn como servidor WSGI
- Crearemos un script de inicio para la aplicación
- Documentaremos el proceso de instalación y configuración
- Verificaremos el funcionamiento en el entorno de despliegue

## Lógica para Evaluar Expresiones

La evaluación de expresiones se realizará en dos pasos:

1. **Envío a la API de OpenAI**: La expresión ingresada por el usuario se enviará a la API junto con la definición de los conjuntos.

2. **Procesamiento de la respuesta**: La respuesta de la API se procesará para extraer:
   - Los elementos que cumplen con la expresión
   - Las regiones del diagrama que deben colorearse
   - Cualquier error o feedback para el usuario

## Generación del Diagrama de Venn

El diagrama de Venn se generará como un SVG con las siguientes características:

1. **Estructura base**: Tres círculos que representan los conjuntos A, B y C.

2. **Regiones**: Siete regiones distintas que representan todas las posibles intersecciones.

3. **Coloración**: Las regiones que cumplen con la expresión se colorearán según la respuesta de la API.

4. **Etiquetas**: Cada región mostrará los elementos que contiene.

## Ejemplo de Flujo Completo

1. El usuario ingresa la expresión "A or B" y hace clic en el botón "Evaluar".

2. La aplicación envía la expresión a la API de OpenAI junto con la definición de los conjuntos.

3. La API evalúa la expresión y devuelve:
   ```json
   {
     "elementos": [1, 2, 4, 5, 6, 7],
     "regiones": ["A∩¬B∩¬C", "¬A∩B∩¬C", "A∩B∩¬C", "A∩¬B∩C", "¬A∩B∩C", "A∩B∩C"],
     "error": null
   }
   ```

4. La aplicación procesa la respuesta y genera un diagrama de Venn con las regiones correspondientes coloreadas.

5. El diagrama se muestra al usuario junto con la lista de elementos que cumplen con la expresión.