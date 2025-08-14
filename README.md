# ProyectoVenn

Aplicación web en Flask que interpreta expresiones de teoría de conjuntos con tres conjuntos fijos A, B y C, y muestra el resultado pintado en un diagrama de Venn de 3 conjuntos. Pensado para docencia: admite desde expresiones simples hasta combinaciones anidadas, con visualización clara de las regiones que cumplen con la expresión.

## Descripción

Esta aplicación permite a los usuarios ingresar expresiones de teoría de conjuntos (como "A or B", "A and B", "(A and B) or (not A and C)", etc.) y visualiza el resultado en un diagrama de Venn de 3 conjuntos. Los conjuntos A, B y C tienen valores fijos predefinidos, y cada región del diagrama de Venn tendrá al menos un elemento.

### Conjuntos Predefinidos

- **Conjunto A**: {1, 4, 6, 7}
- **Conjunto B**: {2, 4, 5, 7}
- **Conjunto C**: {3, 5, 6, 7}

## Documentación

El proyecto está organizado en varios documentos que detallan diferentes aspectos de la implementación:

1. [Arquitectura](arquitectura.md) - Descripción general de la arquitectura del sistema, componentes principales y flujo de datos.

2. [Detalles de Implementación](detalles_implementacion.md) - Información detallada sobre la implementación de cada hito del proyecto.

3. [Ejemplos de Expresiones](ejemplos_expresiones.md) - Ejemplos de expresiones que la aplicación debe poder manejar, junto con los resultados esperados.

4. [Instrucciones para el Prompt de OpenAI](instrucciones_prompt.md) - Guía para crear el prompt que se enviará a la API de OpenAI para evaluar expresiones.

5. [Instrucciones para el Diagrama de Venn](instrucciones_diagrama_venn.md) - Detalles sobre cómo implementar el generador de diagramas de Venn usando SVG.

## Plan de Implementación

El proyecto se implementará en 6 hitos principales:

1. **Configuración inicial del proyecto**
   - Crear estructura básica del proyecto Flask
   - Configurar entorno virtual y dependencias

2. **Implementación de la interfaz básica**
   - Crear plantillas HTML
   - Implementar rutas básicas en Flask

3. **Integración con la API de OpenAI**
   - Implementar conexión con la API
   - Procesar expresiones y respuestas

4. **Implementación del generador de diagramas de Venn**
   - Crear visualización SVG
   - Colorear regiones según la expresión

5. **Pruebas y refinamiento**
   - Probar con diferentes expresiones
   - Mejorar la experiencia del usuario

6. **Despliegue**
   - Preparar la aplicación para producción
   - Documentar el proceso de instalación

## Requisitos

- Python 3.7+
- Flask
- OpenAI API Key
- Navegador web moderno con soporte para SVG

## Instalación (Futura)

1. Clonar el repositorio
2. Crear un entorno virtual: `python -m venv venv`
3. Activar el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Instalar dependencias: `pip install -r requirements.txt`
5. Crear archivo `.env` con la clave de API de OpenAI
6. Ejecutar la aplicación: `flask run`

## Uso (Futuro)

1. Acceder a la aplicación en el navegador (por defecto: http://localhost:5000)
2. Ingresar una expresión de teoría de conjuntos en el campo de texto
3. Hacer clic en el botón "Evaluar"
4. Ver el resultado en el diagrama de Venn

## Licencia

[Incluir información de licencia aquí]
