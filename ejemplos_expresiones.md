# Ejemplos de Expresiones para Diagramas de Venn

Este documento contiene ejemplos de expresiones de teoría de conjuntos que la aplicación debería poder manejar, junto con los resultados esperados. Estos ejemplos servirán como casos de prueba durante el desarrollo.

## Recordatorio de los Conjuntos

- **Conjunto A**: {1, 4, 6, 7}
- **Conjunto B**: {2, 4, 5, 7}
- **Conjunto C**: {3, 5, 6, 7}

## Expresiones Simples

### 1. Conjunto A

**Expresión**: `A`

**Resultado esperado**:
- Elementos: 1, 4, 6, 7
- Regiones coloreadas: A∩¬B∩¬C, A∩B∩¬C, A∩¬B∩C, A∩B∩C

### 2. Conjunto B

**Expresión**: `B`

**Resultado esperado**:
- Elementos: 2, 4, 5, 7
- Regiones coloreadas: ¬A∩B∩¬C, A∩B∩¬C, ¬A∩B∩C, A∩B∩C

### 3. Conjunto C

**Expresión**: `C`

**Resultado esperado**:
- Elementos: 3, 5, 6, 7
- Regiones coloreadas: ¬A∩¬B∩C, A∩¬B∩C, ¬A∩B∩C, A∩B∩C

## Operaciones Básicas

### 4. Unión (A or B)

**Expresión**: `A or B`

**Resultado esperado**:
- Elementos: 1, 2, 4, 5, 6, 7
- Regiones coloreadas: A∩¬B∩¬C, ¬A∩B∩¬C, A∩B∩¬C, A∩¬B∩C, ¬A∩B∩C, A∩B∩C

### 5. Intersección (A and B)

**Expresión**: `A and B`

**Resultado esperado**:
- Elementos: 4, 7
- Regiones coloreadas: A∩B∩¬C, A∩B∩C

### 6. Complemento (not A)

**Expresión**: `not A`

**Resultado esperado**:
- Elementos: 2, 3, 5
- Regiones coloreadas: ¬A∩B∩¬C, ¬A∩¬B∩C, ¬A∩B∩C

### 7. Diferencia (A and not B)

**Expresión**: `A and not B`

**Resultado esperado**:
- Elementos: 1, 6
- Regiones coloreadas: A∩¬B∩¬C, A∩¬B∩C

## Expresiones Compuestas

### 8. Unión de Intersecciones ((A and B) or (A and C))

**Expresión**: `(A and B) or (A and C)`

**Resultado esperado**:
- Elementos: 4, 6, 7
- Regiones coloreadas: A∩B∩¬C, A∩¬B∩C, A∩B∩C

### 9. Intersección de Uniones ((A or B) and (B or C))

**Expresión**: `(A or B) and (B or C)`

**Resultado esperado**:
- Elementos: 2, 4, 5, 6, 7
- Regiones coloreadas: ¬A∩B∩¬C, A∩B∩¬C, A∩¬B∩C, ¬A∩B∩C, A∩B∩C

### 10. Expresión con Negación ((A or B) and not C)

**Expresión**: `(A or B) and not C`

**Resultado esperado**:
- Elementos: 1, 2, 4
- Regiones coloreadas: A∩¬B∩¬C, ¬A∩B∩¬C, A∩B∩¬C

### 11. Diferencia Simétrica (A xor B)

**Expresión**: `(A and not B) or (B and not A)`

**Resultado esperado**:
- Elementos: 1, 2, 5, 6
- Regiones coloreadas: A∩¬B∩¬C, ¬A∩B∩¬C, A∩¬B∩C, ¬A∩B∩C

## Expresiones Complejas

### 12. Expresión Anidada ((A and B) or (not A and C))

**Expresión**: `(A and B) or (not A and C)`

**Resultado esperado**:
- Elementos: 3, 4, 5, 7
- Regiones coloreadas: ¬A∩¬B∩C, A∩B∩¬C, ¬A∩B∩C, A∩B∩C

### 13. Expresión con Múltiples Operadores ((A or B) and not (B and C))

**Expresión**: `(A or B) and not (B and C)`

**Resultado esperado**:
- Elementos: 1, 2, 4, 6
- Regiones coloreadas: A∩¬B∩¬C, ¬A∩B∩¬C, A∩B∩¬C, A∩¬B∩C

### 14. Universo (A or B or C)

**Expresión**: `A or B or C`

**Resultado esperado**:
- Elementos: 1, 2, 3, 4, 5, 6, 7
- Regiones coloreadas: A∩¬B∩¬C, ¬A∩B∩¬C, ¬A∩¬B∩C, A∩B∩¬C, A∩¬B∩C, ¬A∩B∩C, A∩B∩C

### 15. Conjunto Vacío (A and not A)

**Expresión**: `A and not A`

**Resultado esperado**:
- Elementos: ninguno
- Regiones coloreadas: ninguna

## Notas para la Implementación

1. La aplicación debe poder manejar paréntesis para establecer la precedencia de operaciones.
2. Los operadores soportados deben incluir:
   - `and` (intersección)
   - `or` (unión)
   - `not` (complemento)
3. La aplicación debe ser capaz de interpretar expresiones con múltiples operadores y paréntesis anidados.
4. Se debe proporcionar feedback claro cuando una expresión es inválida o tiene errores de sintaxis.