import os
import sys
sys.path.insert(0, r"C:\kgl\lib")

import shutil
from ultralytics import YOLO

def train_express():
    print("Iniciando entrenamiento formal de YOLOv8 para la Maestría...")
    
    # Asegurar que data.yaml exista
    yaml_path = os.path.join("data", "raw", "data.yaml")
    if not os.path.exists(yaml_path):
        import yaml
        data_config = {
            'path': os.path.abspath('data/raw'),
            'train': 'train/images',
            'val': 'valid/images',
            'test': 'test/images',
            'names': {0: 'license_plate'}
        }
        with open(yaml_path, 'w') as f:
            yaml.dump(data_config, f, default_flow_style=False)
        print("data.yaml creado automáticamente.")
        
    model = YOLO("yolov8n.pt")
    
    # Entrenamiento formal: 25 epochs con early stopping
    results = model.train(
        data=yaml_path,
        epochs=25,
        patience=5,
        imgsz=640,
        batch=16,
        name="license_plate_maestria"
    )
    
    # Copiar best.pt a models/best.pt
    source_weight = os.path.join("runs", "detect", "license_plate_maestria", "weights", "best.pt")
    target_weight = os.path.join("models", "best.pt")
    
    if os.path.exists(source_weight):
        os.makedirs("models", exist_ok=True)
        shutil.copy2(source_weight, target_weight)
        print(f"Modelo guardado exitosamente en: {target_weight}")
    else:
        print("Error: No se encontró el modelo entrenado en runs/detect.")

if __name__ == "__main__":
    train_express()
