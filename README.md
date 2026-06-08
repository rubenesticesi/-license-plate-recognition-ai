# Sistema Inteligente de Reconocimiento de Placas (ALPR) con IA

**Proyecto de Maestría - Análisis de un Problema Real y Propuesta de Solución con Inteligencia Artificial**

**Desarrollado por:**
* Edwin Perez
* Ruben Sabogal
* Cristian Quebrada

---

## 1. Descripción del Problema Seleccionado

**Contexto:** Seguridad y control de acceso vehicular en el Valle del Cauca (Cali y municipios aledaños).
**Problema:** En el Valle del Cauca, la gestión del tráfico, el control de acceso a zonas restringidas (conjuntos residenciales, centros empresariales) y la seguridad vial (identificación de vehículos robados o evasores en peajes) dependen en gran medida de procesos manuales o tecnologías obsoletas (como tarjetas RFID físicas que se prestan o pierden). 
La verificación visual por parte de guardas de seguridad es propensa a errores humanos, lenta en horas pico y no deja un registro digital automático e inmutable que sirva como evidencia en caso de incidentes de seguridad (robos, fugas).

## 2. Análisis y Descomposición del Problema

Desglosando la problemática bajo los enfoques vistos en clase, identificamos los siguientes componentes clave:
*   **Cuello de botella operativo:** El registro manual de placas en garitas o peajes toma entre 15 y 30 segundos por vehículo, generando congestión.
*   **Vulnerabilidad de seguridad:** Las tarjetas de acceso físicas no validan la identidad real del vehículo (una tarjeta robada abre la puerta a cualquier auto).
*   **Gestión de datos deficiente:** Las bitácoras manuales (papel y lápiz) dificultan el cruce de datos con bases de datos policiales (vehículos reportados).
*   **Altos costos:** Dependencia excesiva de talento humano 24/7 para labores repetitivas de observación.

## 3. Identificación de Oportunidades de Aplicación de Inteligencia Artificial

La visión por computadora y el Deep Learning ofrecen una oportunidad perfecta para resolver esto. La IA puede:
1.  **Detección de Objetos en Tiempo Real:** Identificar dónde está exactamente la placa en la imagen de un vehículo, independientemente del ángulo o tamaño.
2.  **Reconocimiento Óptico de Caracteres (OCR):** Extraer los caracteres alfanuméricos de la imagen recortada de la placa, transformándolos en texto digital estructurado.
3.  **Validación y Automatización:** Cruzar instantáneamente la placa leída con una base de datos para abrir una barrera o generar una alerta de seguridad.

## 4. Propuesta de Solución Sustentada

Se propone implementar un **Sistema Automático de Reconocimiento de Placas (ALPR)** basado en Inteligencia Artificial. La solución tecnológica se compone de un pipeline de Machine Learning de dos etapas:

1.  **Modelo de Detección (YOLOv8):** Se entrenó un modelo YOLOv8 (You Only Look Once) personalizado utilizando un dataset de más de 20,000 imágenes de vehículos. YOLOv8 fue elegido por su arquitectura *State-of-the-Art* que permite inferencia ultrarrápida (ideal para cámaras en vivo) y alta precisión en la detección de *Bounding Boxes* (Cajas Delimitadoras) alrededor de las placas.
2.  **Modelo de Lectura (EasyOCR):** Una vez la placa es detectada y recortada, la imagen resultante pasa por EasyOCR (basado en Redes Neuronales Convolucionales y Recurrentes - CRNN) para convertir los píxeles en texto (ej. "ABC-123").
3.  **Infraestructura:** La inferencia se empaquetó en una API RESTful construida con **FastAPI**, servida mediante una interfaz web interactiva (HTML/CSS/JS) para uso de operadores en garitas de seguridad.

## 5. Análisis de Posibles Limitaciones o Alcances

**Limitaciones:**
*   **Factores ambientales:** Lluvia extrema, niebla o deslumbramiento del sol directo en la cámara pueden reducir drásticamente la efectividad del OCR.
*   **Estado físico de las placas:** Placas desgastadas, alteradas deliberadamente, cubiertas de barro o dobladas pueden generar falsos negativos.
*   **Hardware:** Para lograr inferencia en tiempo real (30 FPS) en un entorno de producción masivo, se requiere hardware especializado (GPUs Nvidia dedicadas), lo que aumenta los costos de implementación frente a cámaras tradicionales.

**Alcances:**
*   El MVP actual procesa imágenes estáticas con alta precisión. 
*   Está diseñado modularmente para, a futuro, conectar flujos de video RTSP de cámaras IP existentes sin cambiar el núcleo del modelo entrenado.

## 6. Conclusiones y Reflexiones Finales

El desarrollo de esta solución demuestra que la IA no es solo una tecnología emergente, sino una herramienta madura y accesible para resolver ineficiencias del mundo real. Al reemplazar la verificación manual por un pipeline YOLOv8+OCR, no solo se acelera un proceso operativo, sino que se crea un ecosistema de datos digital: cada placa leída puede auditarse y analizarse en tiempo real. 

La principal reflexión es que el éxito de la IA no recae solo en el algoritmo, sino en la **calidad de los datos** (las 20,000 imágenes anotadas fueron críticas para que YOLOv8 aprendiera) y en el diseño del pipeline (combinar detección + OCR en lugar de un solo paso mejora el rendimiento drásticamente).

---

## 🚀 PUNTOS EXTRA (Cumplimiento de Rúbrica)

### MVP (+1 Punto)
Este repositorio contiene el **Producto Mínimo Viable (MVP) 100% funcional**. 
El MVP consta de:
*   Un modelo YOLOv8 entrenado (`models/best.pt`) con mAP50 de 97.3%.
*   Un backend en FastAPI que expone el endpoint predictivo.
*   Una interfaz web *Frontend* donde un usuario puede cargar la imagen de un vehículo y ver la placa reconocida, su probabilidad de acierto y la caja delimitadora en segundos.

### Lean Canvas (+1 Punto)

| Problema | Solución | Propuesta de Valor Única | Ventaja Injusta | Segmentos de Clientes |
| :--- | :--- | :--- | :--- | :--- |
| - Congestión vehicular en accesos.<br>- Suplantación y uso de tarjetas RFID robadas.<br>- Altos costos en vigilancia manual 24/7. | - Sistema ALPR basado en YOLOv8 + OCR.<br>- API integrable con talanqueras y bases de datos.<br>- Dashboard de monitoreo en tiempo real. | Automatizar el 100% del registro vehicular y control de acceso mediante IA ultrarrápida y precisa, eliminando la necesidad de tarjetas físicas y reduciendo tiempos de espera de minutos a segundos. | Pipeline de IA entrenado específicamente y optimizado para funcionar on-premise (sin depender de nube externa), garantizando privacidad y baja latencia. | - Conjuntos residenciales y condominios.<br>- Centros empresariales/Parqueaderos privados.<br>- Peajes departamentales del Valle del Cauca.<br>- Policía / Secretarías de tránsito. |
| **Alternativas Existentes:**<br>- Tarjetas RFID magnéticas.<br>- Bitácoras manuales de guardas.<br>- Cámaras LPR tradicionales (costosas y cerradas). | **Métricas Clave:**<br>- % de Precisión en lectura de placas (Accuracy).<br>- Tiempo de inferencia (ms por vehículo).<br>- Reducción de filas/tiempo de espera en garitas. | **Canales:**<br>- Venta directa a empresas de seguridad privada.<br>- Alianzas con integradores de hardware (empresas que instalan talanqueras y cámaras IP). | **Estructura de Costes:**<br>- Entrenamiento de modelos de IA.<br>- Servidores de inferencia (GPUs).<br>- Desarrollo y mantenimiento de la plataforma Web/API. | **Flujos de Ingreso:**<br>- Suscripción mensual (SaaS) por cámara conectada al sistema.<br>- Setup fee inicial (Instalación y configuración del servidor local). |

---

## Estructura del Repositorio (Para Evaluación)

*   `models/best.pt`: Archivo del modelo de IA entrenado (YOLOv8).
*   `src/api/`: Backend en FastAPI que sirve las predicciones.
*   `src/detection/`: Scripts de inferencia de la Inteligencia Artificial.
*   `src/ocr/`: Lógica de extracción de texto usando EasyOCR.
*   `web/`: Interfaz gráfica de usuario del MVP.
*   `train_express.py`: Script utilizado para el entrenamiento de la red neuronal.
