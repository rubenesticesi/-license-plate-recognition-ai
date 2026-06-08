import os
import pandas as pd
from src.detection.predict_plate import detect_license_plate
from src.ocr.read_plate import read_plate_text
from src.utils.visualization import draw_bbox_and_text

def run_alpr_pipeline(image_path: str) -> dict:
    """
    Ejecuta el pipeline completo: detección -> recorte -> OCR -> validación.
    """
    # Asegurar que el directorio de salida existe
    os.makedirs("outputs/predictions", exist_ok=True)
    
    # 1. Detección
    detections = detect_license_plate(image_path)
    
    if not detections:
        return {
            "image_path": image_path,
            "plate_detected": False,
            "plate_text": None,
            "detection_confidence": 0.0,
            "ocr_confidence": 0.0,
            "valid_format": False,
            "output_image": image_path
        }
        
    # Asumimos la placa con mayor confianza (usualmente la principal en la foto)
    best_detection = max(detections, key=lambda x: x["confidence"])
    
    # 2. OCR
    ocr_result = read_plate_text(best_detection["crop_path"])
    
    # 3. Visualización y guardado
    base_name = os.path.basename(image_path)
    output_image_path = os.path.join("outputs", "predictions", f"pred_{base_name}")
    
    draw_bbox_and_text(
        image_path=image_path,
        output_path=output_image_path,
        bbox=best_detection["bbox"],
        text=ocr_result["plate_text"],
        confidence=ocr_result["ocr_confidence"]
    )
    
    result = {
        "image_path": image_path,
        "plate_detected": True,
        "plate_text": ocr_result["plate_text"],
        "detection_confidence": best_detection["confidence"],
        "ocr_confidence": ocr_result["ocr_confidence"],
        "valid_format": ocr_result["is_valid_format"],
        "output_image": output_image_path
    }
    
    return result

def process_batch_and_save(image_paths: list, output_csv: str = "outputs/results.csv"):
    """
    Procesa un lote de imágenes y guarda los resultados en un CSV.
    """
    results = []
    for path in image_paths:
        res = run_alpr_pipeline(path)
        results.append(res)
        
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    print(f"Resultados guardados en {output_csv}")
    return df

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ALPR Pipeline")
    parser.add_argument("--image", type=str, required=True, help="Ruta de la imagen a procesar")
    args = parser.parse_args()
    
    res = run_alpr_pipeline(args.image)
    print(res)
