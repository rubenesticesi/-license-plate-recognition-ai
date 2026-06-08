# Arquitectura del Sistema ALPR

La arquitectura del sistema de Reconocimiento Automático de Placas (ALPR) sigue un enfoque de pipeline secuencial, donde la salida de una etapa es la entrada de la siguiente.

## Diagrama Textual del Flujo

```text
[ Entrada de Datos ]
   │
   ├──> Imagen Original (UI Streamlit o Script Local)
   │
   v
[ Módulo de Detección - YOLOv8 ]
   │
   ├──> Inferencia del modelo (yolov8n.pt fine-tuned)
   ├──> Extracción de Bounding Box [x1, y1, x2, y2]
   │
   v
[ Módulo de Preprocesamiento de Imagen ]
   │
   ├──> Recorte de la imagen (Crop)
   ├──> Conversión a Escala de Grises
   ├──> Redimensionamiento (x2)
   ├──> Difuminado Gaussiano (reducción de ruido)
   │
   v
[ Módulo de OCR - EasyOCR ]
   │
   ├──> Extracción de texto alfanumérico
   ├──> Obtención de confianza (Confidence score)
   │
   v
[ Módulo de Limpieza y Validación ]
   │
   ├──> Limpieza (Quitar espacios, caracteres especiales)
   ├──> Correcciones heurísticas (ej. 0 por O)
   ├──> Validación Regex (ej. ABC123 para Colombia)
   │
   v
[ Salida y UI ]
   │
   ├──> Guardado de resultados en CSV (outputs/results.csv)
   └──> Visualización en interfaz web (Streamlit) con bounding boxes dibujados
```

## Componentes Tecnológicos
- **Backend Core**: Python 3.x
- **Framework ML Detección**: Ultralytics (YOLOv8)
- **Framework OCR**: EasyOCR (PyTorch)
- **Procesamiento de Imagen**: OpenCV (`cv2`)
- **Interfaz de Usuario (MVP)**: Streamlit
- **Manejo de Datos**: Pandas, NumPy
