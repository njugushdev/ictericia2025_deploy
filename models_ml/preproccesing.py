"""
Utilidades de preprocesamiento para la inferencia de imágenes de ictericia neonatal.
Aplica redimensionamiento, normalización y enmascaramiento de regiones amarillas.
"""

import numpy as np
import cv2
from PIL import Image

# ============================================================
# Constantes globales
# ============================================================
IMG_SIZE = 128          # Tamaño de entrada del modelo
Y_MEAN, Y_STD = 11.21, 5.21  # Estadísticas de normalización del entrenamiento del modelo de regresión


# ============================================================
# Preprocesamiento de imágenes para la inferencia
# ============================================================
def preprocess_for_inference(pil_image):
    """
    Prepara una imagen PIL para ambos modelos (clasificación y regresión).
    Pasos:
      1. Convierte a matriz numpy RGB
      2. Redimensiona a 128x128 píxeles
      3. Normaliza los valores de píxeles al rango [0,1]
      4. Crea una máscara amarilla basada en el espacio de color HSV
      5. Concatena RGB + máscara → (1,128,128,4)
    """
    if isinstance(pil_image, str):
        pil_image = Image.open(pil_image).convert("RGB")

    img = np.array(pil_image.convert("RGB"))
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE)).astype(np.float32) / 255.0

    # Máscara amarilla basada en HSV
    hsv = cv2.cvtColor((img * 255).astype(np.uint8), cv2.COLOR_RGB2HSV)
    lower_yellow = np.array([15, 40, 40])
    upper_yellow = np.array([35, 255, 255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow).astype(np.float32) / 255.0
    yellow_mask = np.expand_dims(yellow_mask, axis=-1)

    # Combinar en un tensor de 4 canales (RGB + máscara amarilla)
    img_4ch = np.concatenate([img, yellow_mask], axis=-1)
    img_4ch = np.expand_dims(img_4ch, axis=0)
    return img_4ch.astype(np.float32)


# ============================================================
# Postprocesamiento de la salida de regresión
# ============================================================
def denormalize_bilirubin(pred_norm):
    """Convierte la salida normalizada del modelo de regresión a mg/dL."""
    return (pred_norm * Y_STD) + Y_MEAN