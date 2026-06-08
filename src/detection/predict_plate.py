import os
import cv2
from ultralytics import YOLO

def detect_license_plate(image_path: str, model_path: str = "models/best.pt") -> list:
    """
    Detecta la región de la placa en una imagen usando YOLOv8.
    Retorna una lista de diccionarios con la información de cada placa detectada.
    """
    if not os.path.exists(model_path):
        print(f"Advertencia: No se encontró el modelo {model_path}. Usando fallback para leer toda la imagen con OCR.")

        img = cv2.imread(image_path)
        if img is not None:
            h, w = img.shape[:2]
            return [{
                "bbox": [0, 0, w, h],
                "confidence": 1.0,
                "crop_path": image_path
            }]
        return []
        
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Imagen no encontrada: {image_path}")

    # Asegurar que el directorio de salida para recortes existe
    os.makedirs("outputs/crops", exist_ok=True)

    # Cargar modelo
    model = YOLO(model_path)
    
    # Realizar inferencia
    results = model(image_path)
    
    # Cargar imagen original para recortar
    img = cv2.imread(image_path)
    base_name = os.path.basename(image_path).split('.')[0]
    
    detections = []
    
    for r in results:
        boxes = r.boxes
        for i, box in enumerate(boxes):
            # Obtener coordenadas del bounding box (formato xyxy)
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            confidence = float(box.conf[0].cpu().numpy())
            
            # Recortar la región de la placa
            # Añadir un pequeño margen (padding) si es posible
            h, w = img.shape[:2]
            px1, py1 = max(0, x1 - 5), max(0, y1 - 5)
            px2, py2 = min(w, x2 + 5), min(h, y2 + 5)
            
            crop_img = img[py1:py2, px1:px2]
            
            # Guardar recorte
            crop_filename = f"{base_name}_crop_{i}.jpg"
            crop_path = os.path.join("outputs", "crops", crop_filename)
            cv2.imwrite(crop_path, crop_img)
            
            detections.append({
                "image_path": image_path,
                "crop_path": crop_path,
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2]
            })
            
    return detections

if __name__ == "__main__":
    # Prueba rápida
    # Asegúrate de tener una imagen y el modelo
    # res = detect_license_plate("data/sample/car.jpg")
    # print(res)
    pass
