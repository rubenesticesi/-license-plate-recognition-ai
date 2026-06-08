# Informe Académico: Sistema de Reconocimiento Automático de Placas Vehiculares

## 1. Título del Proyecto
Sistema de Reconocimiento Automático de Placas Vehiculares mediante Visión por Computador y Redes Neuronales Convolucionales (YOLOv8 + EasyOCR).

## 2. Descripción del Problema
La identificación manual de vehículos en controles de acceso, peajes y parqueaderos genera cuellos de botella, errores humanos de transcripción y demoras en la trazabilidad. No contar con un registro digital automatizado impide la integración con sistemas de seguridad y facturación en tiempo real.

## 3. Contexto del Problema
En el Valle del Cauca, el flujo de vehículos en conjuntos residenciales, universidades y centros logísticos es alto. La gestión de acceso depende frecuentemente de personal de seguridad anotando manualmente las placas o entregando tiquetes físicos. Esta práctica no solo es lenta, sino que vulnera la seguridad al no permitir validaciones instantáneas con bases de datos de vehículos autorizados o reportados.

## 4. Análisis y Descomposición del Problema
El problema se divide en tres componentes principales:
- **Detección**: Encontrar dónde está ubicada la placa en la imagen de un vehículo, independientemente de las condiciones de luz o el ángulo.
- **Reconocimiento Óptico (OCR)**: Extraer los caracteres de la región recortada de la placa y convertirlos a texto digital.
- **Validación y Almacenamiento**: Confirmar que el texto extraído obedece al formato de placa local y registrar el evento.

## 5. Oportunidad de Aplicación de IA
La Inteligencia Artificial, específicamente la Visión por Computador, ofrece soluciones robustas como YOLO (You Only Look Once) para la detección de objetos en tiempo real con alta precisión, y modelos OCR basados en Deep Learning para la extracción de texto, lo que permite automatizar por completo el proceso de identificación.

## 6. Descripción del Dataset
Se utiliza como fuente primaria el "Automatic License Plate Recognition ALPR Dataset" de Kaggle (mgmitesh). 
Contiene imágenes de vehículos con sus respectivas etiquetas (bounding boxes) en formato YOLO.
Como respaldo académico y para futuros ajustes al contexto latinoamericano, se documenta el dataset **UFPR-ALPR**, que incluye miles de imágenes capturadas en escenarios reales en Brasil.

## 7. Metodología CRISP-DM
1. **Business Understanding (Comprensión del Negocio)**: Reducir tiempos de espera en controles de acceso vehicular y mejorar la trazabilidad y seguridad en el Valle del Cauca.
2. **Data Understanding (Comprensión de Datos)**: Análisis exploratorio de imágenes de vehículos, validando formatos de anotación y distribución en conjuntos de entrenamiento, validación y prueba.
3. **Data Preparation (Preparación de Datos)**: Creación de archivos `data.yaml` y preprocesamiento de recortes (escala de grises, redimensionamiento, difuminado) para mejorar el rendimiento del OCR.
4. **Modeling (Modelado)**: Fine-tuning de YOLOv8n sobre las imágenes etiquetadas y aplicación de EasyOCR.
5. **Evaluation (Evaluación)**: Medición del mAP50 de YOLOv8 y la confianza de las predicciones del OCR.
6. **Deployment (Despliegue)**: Construcción de un MVP interactivo usando Streamlit.

## 8. Arquitectura de Solución
La solución consta de un flujo secuencial (pipeline):
1. Captura/Carga de imagen.
2. Inferencia con YOLOv8.
3. Recorte de la ROI (Region of Interest).
4. Preprocesamiento de la imagen recortada.
5. Inferencia con EasyOCR.
6. Limpieza, formateo y validación de expresiones regulares.
7. Almacenamiento estructurado (CSV) y visualización en UI (Streamlit).

## 9. Modelo Seleccionado
- **Detección**: YOLOv8 (versión Nano o Small). Se selecciona por su balance excepcional entre velocidad de inferencia y precisión, ideal para procesar frames de video en tiempo real en un futuro.
- **OCR**: EasyOCR. Se selecciona por ser open-source, soportar múltiples idiomas y basarse en redes neuronales (CRNN + CTC) que toleran cierto nivel de distorsión.

## 10. Métricas de Evaluación
- **Detección**: Precision, Recall, mAP50 (Mean Average Precision al 50% de IoU).
- **OCR**: Nivel de confianza promedio devuelto por EasyOCR (probabilidad softmax) y exactitud de caracteres (Character Error Rate - CER) si se contara con ground truth de texto.

## 11. Resultados Esperados del MVP
Un prototipo funcional (MVP) que, dada la imagen de un vehículo, logre detectar la placa y retornar el texto alfanumérico en menos de 2 segundos con al menos un 85% de precisión conjunta.

## 12. Limitaciones
- Placas sucias, dañadas o bloqueadas parcialmente.
- Condiciones de iluminación extremas (reflejos fuertes o visión nocturna sin cámara infrarroja).
- Ángulos de cámara demasiado pronunciados.

## 13. Alcance
El MVP procesa imágenes estáticas una por una a través de una interfaz web. No incluye lectura de video en tiempo real RTSP ni integración con bases de datos SQL o motores de reglas de negocio complejos, lo cual queda para fases productivas.

## 14. Consideraciones Éticas y Legales
La captura sistemática de placas vehiculares en espacios públicos o privados debe regirse bajo la Ley de Protección de Datos Personales (Ley 1581 de 2012 en Colombia). Los datos deben ser usados estrictamente para el propósito de control y seguridad autorizado, garantizando su confidencialidad.

## 15. Conclusiones
La combinación de YOLOv8 y EasyOCR conforma una solución de bajo costo computacional (relativo) y alta eficacia para resolver un problema cotidiano. El proceso de MLOps básico implementado permite escalar y mejorar los modelos con nuevos datos locales fácilmente.

## 16. Trabajo Futuro
- Entrenar un modelo de reconocimiento de caracteres (OCR) específico para la tipografía de placas colombianas.
- Integrar procesamiento de flujos de video (RTSP) usando OpenCV o GStreamer.
- Desplegar el modelo en dispositivos edge (ej. Raspberry Pi o NVIDIA Jetson).
