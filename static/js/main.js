document.addEventListener('DOMContentLoaded', function() {
    // Obtener el formulario
    const form = document.getElementById('expression-form');
    
    // Agregar un event listener para el envío del formulario
    if (form) {
        form.addEventListener('submit', function(event) {
            // Prevenir el comportamiento por defecto del formulario
            event.preventDefault();
            
            // Obtener el valor de la expresión
            const expressionInput = document.getElementById('expression');
            const expression = expressionInput.value.trim();
            
            // Validar que la expresión no esté vacía
            if (!expression) {
                alert('Por favor, ingresa una expresión.');
                return;
            }
            
            // Mostrar un mensaje de carga
            const vennDiagram = document.getElementById('venn-diagram');
            if (vennDiagram) {
                vennDiagram.innerHTML = `
                    <div class="placeholder-message">
                        <p>Evaluando expresión: <strong>${expression}</strong></p>
                        <p>Por favor, espera un momento...</p>
                    </div>
                `;
            }
            
            // Deshabilitar el botón mientras se procesa la solicitud
            const submitButton = document.getElementById('evaluate-btn');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Evaluando...';
            }
            
            // Enviar la expresión al servidor para ser evaluada
            fetch('/api/evaluate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ expression: expression }),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error HTTP: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Respuesta recibida:', data);
                
                // Mostrar el resultado
                if (vennDiagram) {
                    if (data.success) {
                        // Mostrar el diagrama SVG
                        vennDiagram.innerHTML = `
                            <div class="result-container">
                                <div class="svg-container">
                                    <--! ${data.svg} -->
                                </div>
                                <div class="result-info">
                                    <h4>Resultado:</h4>
                                    <p><strong>Expresión:</strong> ${expression}</p>
                                    <p><strong>Elementos:</strong> ${data.elementos.join(', ') || 'Ninguno'}</p>
                                    <p><strong>Explicación:</strong> ${data.explicacion}</p>
                                </div>
                            </div>
                        `;
                    } else {
                        // Mostrar mensaje de error
                        vennDiagram.innerHTML = `
                            <div class="error-message">
                                <p><strong>Error:</strong> ${data.error || 'Error desconocido'}</p>
                                <p>${data.explicacion || ''}</p>
                            </div>
                        `;
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                
                // Mostrar mensaje de error
                if (vennDiagram) {
                    vennDiagram.innerHTML = `
                        <div class="error-message">
                            <p><strong>Error:</strong> No se pudo procesar la solicitud</p>
                            <p>Por favor, inténtalo de nuevo más tarde.</p>
                        </div>
                    `;
                }
            })
            .finally(() => {
                // Habilitar el botón nuevamente
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.textContent = 'Evaluar';
                }
            });
        });
    }
});