"""
TEST.py
Prueba rápida de integración de modelos para verificación local antes de ejecutar Streamlit.
Verifica:
 - Carga de modelos (clasificación + regresión)
 - Flujo de preprocesamiento
 - Formato de salida de inferencia
"""

import sys
import os
# Agrega la raíz del proyecto (ictericia2025) al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(_file_), '..')))

from PIL import Image
from core.processor import predict_image
from models_ml.preproccesing import preprocess_for_inference

# === Seleccionar una imagen de muestra ===
SAMPLE_PATH = "C:/Users/PC/ML PROJECTS/Neojaundice/NeoJaundice/images"
if not os.path.exists(SAMPLE_PATH):
    raise FileNotFoundError("❌ Directorio de imágenes no encontrado. Verifica la ruta del dataset.")

sample_files = [f for f in os.listdir(SAMPLE_PATH) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
if not sample_files:
    raise FileNotFoundError("❌ No se encontraron archivos de imagen en NeoJaundice/images.")

test_image_path = os.path.join(SAMPLE_PATH, sample_files[0])
print(f"🧪 Imagen de muestra utilizada: {test_image_path}")

# === Cargar y predecir ===
pil_img = Image.open(test_image_path)
cls_label, prob, bilirubin = predict_image(pil_img)

# === Mostrar resultados ===
print("✅ Inferencia del modelo completada con éxito")
print(f"Clase predicha: {cls_label}")
print(f"Probabilidad: {prob * 100:.1f}%")
print(f"Bilirrubina estimada: {bilirubin} mg/dL")