import cv2
import matplotlib.pyplot as plt

def draw_bbox_and_text(image_path: str, output_path: str, bbox: list, text: str = None, confidence: float = None):
    """
    Dibuja un bounding box y texto sobre una imagen y la guarda.
    
    Args:
        image_path: Ruta de la imagen de entrada
        output_path: Ruta donde guardar la imagen con los dibujos
        bbox: Lista con coordenadas [x1, y1, x2, y2]
        text: Texto a mostrar (ej. placa leída)
        confidence: Confianza de la detección o lectura
    """
    # Cargar la imagen
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"No se pudo cargar la imagen en: {image_path}")
        
    x1, y1, x2, y2 = [int(v) for v in bbox]
    
    # Dibujar el bounding box (Color BGR: Verde)
    color = (0, 255, 0)
    thickness = 2
    cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
    
    # Preparar el texto
    display_text = ""
    if text:
        display_text += text
    if confidence is not None:
        display_text += f" ({confidence:.2f})"
        
    if display_text:
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.9
        font_thickness = 2
        # Dibujar fondo negro para el texto
        (text_width, text_height), _ = cv2.getTextSize(display_text, font, font_scale, font_thickness)
        cv2.rectangle(img, (x1, y1 - text_height - 10), (x1 + text_width, y1), color, -1)
        # Escribir texto (Color BGR: Negro o Blanco)
        cv2.putText(img, display_text, (x1, y1 - 5), font, font_scale, (0, 0, 0), font_thickness)
        
    # Guardar imagen
    cv2.imwrite(output_path, img)
    return output_path
