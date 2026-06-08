import os
import random
import base64
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import mimetypes

# Forzar tipos MIME correctos para Windows
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("application/javascript", ".js")

# Importar el pipeline local
import sys
# Asegurar que src y nuestra carpeta de librerías cortas estén en el path
sys.path.insert(0, r"C:\kgl\lib")
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.pipeline.run_pipeline import run_alpr_pipeline

app = FastAPI(title="ALPR API", version="1.0.0")

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos del frontend (la carpeta web)
web_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "web")
os.makedirs(web_dir, exist_ok=True)
app.mount("/web", StaticFiles(directory=web_dir, html=True), name="static")

@app.get("/")
def redirect_root():
    return RedirectResponse(url="/web/")

@app.get("/web")
def redirect_web():
    return RedirectResponse(url="/web/")

def encode_image_base64(image_path: str) -> str:
    """Convierte una imagen a base64 para enviarla al frontend."""
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded}"

@app.post("/api/predict/upload")
async def predict_upload(file: UploadFile = File(...)):
    """Procesa una imagen subida por el usuario."""
    # Crear carpetas de muestra temporal
    sample_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "sample")
    os.makedirs(sample_dir, exist_ok=True)
    
    file_path = os.path.join(sample_dir, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Correr pipeline
        result = run_alpr_pipeline(file_path)
        
        # Codificar imagen resultante en base64 para mostrarla en el frontend
        if result.get("output_image"):
            result["output_image_b64"] = encode_image_base64(result["output_image"])
            
        return JSONResponse(content=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dataset/validation/random")
def get_random_validation_image():
    """Selecciona y retorna la ruta de una imagen aleatoria del dataset de validación."""
    valid_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "raw", "valid", "images")
    
    if not os.path.exists(valid_dir):
        raise HTTPException(status_code=404, detail="Dataset de validación no encontrado en data/raw/valid/images.")
        
    images = [f for f in os.listdir(valid_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not images:
        raise HTTPException(status_code=404, detail="No se encontraron imágenes en la carpeta de validación.")
        
    random_image = random.choice(images)
    image_path = os.path.join(valid_dir, random_image)
    
    return {"image_name": random_image, "image_path": image_path, "image_b64": encode_image_base64(image_path)}

class DatasetPredictRequest(BaseModel):
    image_path: str

@app.post("/api/predict/dataset")
def predict_dataset(req: DatasetPredictRequest):
    """Procesa una imagen preexistente (ej. de validación)."""
    if not os.path.exists(req.image_path):
        raise HTTPException(status_code=404, detail="Imagen no encontrada en el servidor.")
        
    try:
        result = run_alpr_pipeline(req.image_path)
        
        if result.get("output_image"):
            result["output_image_b64"] = encode_image_base64(result["output_image"])
            
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
