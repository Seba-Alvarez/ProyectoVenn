"""
Módulo para generar diagramas de Venn.
Este módulo se encargará de crear representaciones SVG de diagramas de Venn
basados en las regiones que deben colorearse según la expresión evaluada.
"""

import re

class VennDiagram:
    """Generador de diagramas de Venn."""
    
    def __init__(self):
        """Inicializa el generador de diagramas de Venn."""
        # Definir los conjuntos
        self.conjunto_a = {1, 3, 5, 7}
        self.conjunto_b = {2, 3, 6, 7}
        self.conjunto_c = {4, 5, 6, 7}
        self.conjunto_u = {1,2,3,4,5,6,7}
        
        # Mapeo de regiones a IDs
        self.region_mapping = {
            'A∩¬B∩¬C': 'region-1',  # Solo A
            '¬A∩B∩¬C': 'region-2',  # Solo B
            'A∩B∩¬C': 'region-3',   # A y B, no C
            '¬A∩¬B∩C': 'region-4',  # Solo C
            'A∩¬B∩C': 'region-5',   # A y C, no B
            '¬A∩B∩C': 'region-6',   # B y C, no A
            'A∩B∩C': 'region-7'     # A, B y C
        }
        
        # Mapeo de regiones a elementos
        self.region_elements = {
            'A∩¬B∩¬C': {1},           # Solo A
            '¬A∩B∩¬C': {2},           # Solo B
            'A∩B∩¬C': {3},            # A y B, no C
            '¬A∩¬B∩C': {4},           # Solo C
            'A∩¬B∩C': {5},            # A y C, no B
            '¬A∩B∩C': {6},            # B y C, no A
            'A∩B∩C': {7}              # A, B y C
        }
    
    def  calcular_regiones(self, expresion):
        norm = self.tokenize(expresion)
        reg = eval(norm)
        return reg

    def tokenize(self, s: str):
        print(f"Tokenizando expresión: {s}")
        # normalizamos operadores verbales y símbolos
        replacements = {
            'or': ' | ',
            'and': ' & ',
            'not': ' U - ',
            'A': 'self.conjunto_a',
            'B': 'self.conjunto_b',
            'C': 'self.conjunto_c'
        }

        for k, v in replacements.items():
            s = s.replace(k, v)
        
        return s
        

    def parse(self, expresion: str):
        exp = self.tokenize(expresion)
        return exp
        #result = self.parse_union(expresion)
        #if self.peek() is not None:
        #    raise ValueError(f"Entrada sobrante a partir de: {self.peek()}")
        #return result

    def parse_union(self, expresion: str):
        left = self.parse_diff(expresion)
        while self.peek() == 'OR':
            self.take('OR')
            right = self.parse_diff()
            left = left | right
        return left




def main():
    # Crear el objeto VennDiagram
    diagrama = VennDiagram()
    
    # Ejemplo de expresión (puedes cambiarla según tu lógica)
    expresion = "A or B"
    
    # Llamar al método calcular_regiones
    resultado = diagrama.calcular_regiones(expresion)
    
    # Imprimir el resultado (debería ser None porque el método está vacío)
    print("Resultado de calcular_regiones:", resultado)

if __name__ == '__main__':
    main()















    def generate_svg(self, colored_regions=None, elements=None):
        """
        Genera un diagrama de Venn en formato SVG.
        
        Args:
            colored_regions (list): Lista de regiones que deben colorearse.
            elements (list): Lista de elementos que cumplen con la expresión.
            
        Returns:
            str: Representación SVG del diagrama de Venn.
        """
        # Si no se proporcionan regiones coloreadas, usar una lista vacía
        if colored_regions is None:
            colored_regions = []
        
        # Si no se proporcionan elementos, usar una lista vacía
        if elements is None:
            elements = []
        
        # Convertir las regiones a IDs
        colored_region_ids = [self.region_mapping.get(region, '') for region in colored_regions]
        
        # Posiciones para las etiquetas de elementos en cada región
        element_positions = {
            'region-1': (130, 150),  # Solo A
            'region-2': (270, 150),  # Solo B
            'region-3': (200, 270),  # Solo C
            'region-4': (200, 140),  # A y B, no C
            'region-5': (160, 210),  # A y C, no B
            'region-6': (240, 210),  # B y C, no A
            'region-7': (200, 190)   # A, B y C
        }
        
        # Crear las regiones SVG
        regions_svg = ""
        for region_name, region_id in self.region_mapping.items():
            # Obtener el path para la región
            path = self._get_region_path(region_id)
            
            # Determinar si la región debe colorearse
            is_colored = region_id in colored_region_ids
            class_name = "region" + (" colored" if is_colored else "")
            
            # Añadir el path al SVG
            regions_svg += f'<path id="{region_id}" class="{class_name}" d="{path}" />\n'
            
            # Obtener los elementos de esta región
            region_elements = self.region_elements.get(region_name, set())
            
            # Determinar qué elementos de la región están en la lista de elementos que cumplen la expresión
            matching_elements = [elem for elem in region_elements if elem in elements]
            
            # Si hay elementos que coinciden, mostrarlos
            if matching_elements:
                x, y = element_positions.get(region_id, (0, 0))
                elements_text = ', '.join(str(elem) for elem in matching_elements)
                regions_svg += f'<text class="element" x="{x}" y="{y}" text-anchor="middle">{elements_text}</text>\n'
        
        # Crear el SVG completo
        svg = f"""
<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
    <style>
        .region {{
            fill: transparent;
            stroke: #333;
            stroke-width: 1;
        }}
        .colored {{
            fill: rgba(255, 165, 0, 0.5);
        }}
        .circle-a {{
            stroke: blue;
            stroke-width: 2;
            fill: transparent;
        }}
        .circle-b {{
            stroke: red;
            stroke-width: 2;
            fill: transparent;
        }}
        .circle-c {{
            stroke: green;
            stroke-width: 2;
            fill: transparent;
        }}
        .label {{
            font-family: Arial;
            font-size: 20px;
            font-weight: bold;
        }}
        .element {{
            font-family: Arial;
            font-size: 12px;
            fill: #333;
        }}
    </style>
    
    <!-- Círculos para los conjuntos -->
    <circle class="circle-a" cx="170" cy="170" r="100" />
    <circle class="circle-b" cx="230" cy="170" r="100" />
    <circle class="circle-c" cx="200" cy="230" r="100" />
    
    <!-- Regiones del diagrama -->
    {regions_svg}
    
    <!-- Etiquetas de los conjuntos -->
    <text class="label" x="100" y="120" fill="blue">A</text>
    <text class="label" x="290" y="120" fill="red">B</text>
    <text class="label" x="200" y="320" fill="green">C</text>
</svg>
"""
        
        return svg
    
    def _get_region_path(self, region_id):
        """
        Obtiene el path SVG para una región específica.
        
        Args:
            region_id (str): ID de la región.
            
        Returns:
            str: Path SVG para la región.
        """
        # Esta es una implementación de placeholder
        # La implementación real se hará en el HITO 4
        
        # Mapeo de regiones a paths SVG (aproximados)
        region_paths = {
            'region-1': 'M120,170 A80,80 0 0,1 170,90 A80,80 0 0,1 220,170 A80,80 0 0,1 170,250 A80,80 0 0,1 120,170 Z',
            'region-2': 'M280,170 A80,80 0 0,1 230,90 A80,80 0 0,1 180,170 A80,80 0 0,1 230,250 A80,80 0 0,1 280,170 Z',
            'region-3': 'M200,280 A80,80 0 0,1 120,230 A80,80 0 0,1 200,180 A80,80 0 0,1 280,230 A80,80 0 0,1 200,280 Z',
            'region-4': 'M200,150 A50,50 0 0,1 150,200 A50,50 0 0,1 200,250 A50,50 0 0,1 250,200 A50,50 0 0,1 200,150 Z',
            'region-5': 'M160,220 A40,40 0 0,1 200,180 A40,40 0 0,1 240,220 A40,40 0 0,1 200,260 A40,40 0 0,1 160,220 Z',
            'region-6': 'M240,220 A40,40 0 0,1 200,180 A40,40 0 0,1 160,220 A40,40 0 0,1 200,260 A40,40 0 0,1 240,220 Z',
            'region-7': 'M200,200 A30,30 0 0,1 170,230 A30,30 0 0,1 200,260 A30,30 0 0,1 230,230 A30,30 0 0,1 200,200 Z'
        }
        
        return region_paths.get(region_id, '')