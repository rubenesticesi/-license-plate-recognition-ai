import os
import cv2
import easyocr
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instanciar el lector globalmente para evitar recargarlo en cada llamada
# Usamos español e inglés por si hay caracteres ambiguos
try:
    reader = easyocr.Reader(['en', 'es'], gpu=False)  # Poner gpu=True si hay GPU disponible
except Exception as e:
    logger.error(f"Error al inicializar EasyOCR: {e}")
    reader = None

def preprocess_for_ocr(image_path_or_array):
    """
    Aplica técnicas de procesamiento de imagen a la placa recortada
    para mejorar el rendimiento del OCR. Retorna un array numpy (escala de grises).
    """
    import numpy as np
    if isinstance(image_path_or_array, str):
        img = cv2.imread(image_path_or_array)
    else:
        img = image_path_or_array
        
    if img is None:
        return image_path_or_array
        
    # Convertir a escala de grises si tiene canales
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    
    # Redimensionar (ampliar) suele ayudar a EasyOCR con caracteres pequeños
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # Aplicar difuminado ligero para reducir ruido
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    
    return blur

def read_plate_text(crop_path: str) -> dict:
    """
    Lee el texto de una imagen recortada de una placa usando EasyOCR.
    """
    from src.utils.validators import clean_plate_text, validate_colombian_plate, format_colombian_plate
    
    if not os.path.exists(crop_path):
        return {
            "crop_path": crop_path,
            "plate_text": "",
            "ocr_confidence": 0.0,
            "is_valid_format": False
        }
        
    # Preprocesar imagen y obtener array numpy
    processed_img = preprocess_for_ocr(crop_path)
    
    if reader is None:
        return {
            "crop_path": crop_path,
            "plate_text": "ERROR_OCR_NOT_LOADED",
            "ocr_confidence": 0.0,
            "is_valid_format": False
        }
    
    # Ejecutar OCR directamente sobre el array preprocesado en memoria para evitar errores de deserialización
    results = reader.readtext(processed_img, detail=1)
    
    # Buscar el texto con mayor confianza o concatenar
    best_text = ""
    best_conf = 0.0
    
    # En muchos casos de placas, EasyOCR detecta todo en un solo bloque
    # o en dos bloques (arriba/abajo). Concatenamos o tomamos el mejor.
    all_text = ""
    total_conf = 0.0
    
    for (bbox, text, conf) in results:
        all_text += text + " "
        total_conf += conf
        
        if conf > best_conf:
            best_conf = conf
            best_text = text
            
    # Calculamos la confianza media
    avg_conf = total_conf / len(results) if len(results) > 0 else 0.0
    
    # Limpiar y formatear el texto
    cleaned_text = clean_plate_text(all_text)
    formatted_text = format_colombian_plate(cleaned_text)
    
    # Validar formato
    is_valid = validate_colombian_plate(formatted_text)
    
    return {
        "crop_path": crop_path,
        "plate_text": formatted_text,
        "ocr_confidence": avg_conf,
        "is_valid_format": is_valid
    }

if __name__ == "__main__":
    pass
