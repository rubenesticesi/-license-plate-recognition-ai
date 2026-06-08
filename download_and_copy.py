import os
import shutil

# Definir una ruta corta para la caché de kagglehub y evitar el límite de 260 caracteres de Windows
os.environ['KAGGLEHUB_CACHE'] = "C:\\kgl"

import kagglehub

print("Descargando dataset en ruta corta temporal...")
try:
    path = kagglehub.dataset_download("mgmitesh/automatic-license-plate-recognition-alpr-dataset")
    print("Descargado en:", path)
except Exception as e:
    print(f"Error descargando: {e}")
    exit(1)

# Usamos el prefijo \\?\ para forzar a Windows a aceptar rutas de hasta 32,767 caracteres
target_dir = "\\\\?\\" + os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "raw"))
source_dir = "\\\\?\\" + os.path.abspath(path)

os.makedirs(target_dir, exist_ok=True)

print("Copiando archivos a data/raw...")

# Verificamos si los datos están directamente en root o dentro de una carpeta 'Data'
items = os.listdir(source_dir)
if 'Data' in items and os.path.isdir(os.path.join(source_dir, 'Data')):
    source_dir = os.path.join(source_dir, 'Data')
    items = os.listdir(source_dir)

for item in items:
    s = os.path.join(source_dir, item)
    d = os.path.join(target_dir, item)
    if os.path.isdir(s):
        shutil.copytree(s, d, dirs_exist_ok=True)
    else:
        shutil.copy2(s, d)
        
print("Archivos copiados exitosamente.")
