import re

def clean_plate_text(text: str) -> str:
    """
    Limpia el texto extraído por OCR, convirtiéndolo a mayúsculas,
    eliminando espacios y caracteres especiales, y corrigiendo confusiones comunes.
    """
    # Convertir a mayúsculas y quitar espacios y guiones
    text = text.upper().replace(" ", "").replace("-", "")
    
    # Quitar cualquier caracter que no sea letra o número
    text = re.sub(r'[^A-Z0-9]', '', text)
    
    return text

def validate_colombian_plate(text: str) -> bool:
    """
    Valida si el texto corresponde al formato de una placa colombiana.
    - Carro particular: 3 letras + 3 números (ej. ABC123)
    - Moto: 3 letras + 2 números + 1 letra (ej. ABC12D)
    """
    # Expresiones regulares para placas colombianas
    car_pattern = r'^[A-Z]{3}[0-9]{3}$'
    moto_pattern = r'^[A-Z]{3}[0-9]{2}[A-Z]$'
    
    if re.match(car_pattern, text) or re.match(moto_pattern, text):
        return True
    return False

def format_colombian_plate(text: str) -> str:
    """
    Aplica heurísticas para corregir errores comunes en posiciones específicas
    según el formato esperado. Esto es avanzado, pero en este MVP limpiamos
    y luego validamos.
    """
    text = clean_plate_text(text)
    
    # Asumiendo placa de carro (3 letras, 3 números)
    if len(text) == 6:
        # Corregir letras confundidas con números en las primeras 3 posiciones
        letters_part = text[:3]
        letters_part = letters_part.replace('0', 'O').replace('1', 'I').replace('5', 'S').replace('8', 'B')
        
        # Corregir números confundidos con letras en las posiciones 4 y 5
        # (Y 6 si es carro)
        nums_part = text[3:]
        # Solo corregimos números seguros
        nums_part = nums_part.replace('O', '0').replace('I', '1').replace('S', '5').replace('B', '8')
        
        corrected = letters_part + nums_part
        return corrected
        
    return text
