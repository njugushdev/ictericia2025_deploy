"""
Funciones del procesador para la predicción de ictericia neonatal.
Integra los modelos CNN de clasificación y regresión.
"""
import gdown, os

def ensure_models():
    os.makedirs("models_ml", exist_ok=True)
    
    files = {
        "models_ml/strong_cnn_with_mask_jaundice.h5": "1EbQp7GJPFcDyqF2hSM4rOAmqcTHWs3dN",
        "models_ml/cnn_regression_model_improved.h5": "1B26t7LvgcNp99Nv-9riqVABuUqLzB3g2"
    }

    for path, file_id in files.items():
        if not os.path.exists(path):
            url = f"https://drive.google.com/uc?id={file_id}"
            print(f"⬇️ Downloading {os.path.basename(path)} ...")
            gdown.download(url, path, quiet=False)

# Call this before loading models
ensure_models()

import os
import tensorflow as tf
from tensorflow.keras.metrics import MeanSquaredError
from PIL import Image
from models_ml.preproccesing import preprocess_for_inference, denormalize_bilirubin


# ============================================================
# Rutas e inicialización de los modelos
# ============================================================
CLS_MODEL_PATH = "models_ml/strong_cnn_with_mask_jaundice.h5"
REG_MODEL_PATH = "models_ml/cnn_regression_model_improved.h5"

CUSTOM_OBJECTS = {
    "mse": MeanSquaredError
}

try:
    # Cargar modelo de clasificación
    cls_model = tf.keras.models.load_model(CLS_MODEL_PATH)

    # Cargar modelo de regresión con métrica personalizada
    reg_model = tf.keras.models.load_model(REG_MODEL_PATH, custom_objects=CUSTOM_OBJECTS)

    print("✅ Modelos cargados correctamente:")
    print(f" - Modelo de clasificación: {CLS_MODEL_PATH}")
    print(f" - Modelo de regresión: {REG_MODEL_PATH}")
except Exception as e:
    raise RuntimeError(f"❌ Error al cargar los modelos: {e}")


# ============================================================
# Función de predicción
# ============================================================
def predict_image(pil_image):
    """
    Realiza la inferencia completa:
      1. Preprocesa la imagen (redimensionar, normalizar, aplicar máscara)
      2. Predice la clase (ictericia / no_ictericia)
      3. Predice el nivel de bilirrubina (mg/dL, desnormalizado)
    Retorna:
        tuple (pred_label, probability, bilirubin_value)
    """
    img_input = preprocess_for_inference(pil_image)

    # Clasificación
    cls_prob = float(cls_model.predict(img_input, verbose=0)[0][0])
    cls_label = "ictericia" if cls_prob >= 0.5 else "no_ictericia"

    # Regresión (valor desnormalizado)
    pred_norm = float(reg_model.predict(img_input, verbose=0)[0][0])
    bilirubin_val = round(denormalize_bilirubin(pred_norm), 2)

    return cls_label, cls_prob, bilirubin_val


# ============================================================
# Utilidad de visualización para Streamlit
# ============================================================
def mostrar_imagen_con_prediccion(fila, pred_label, prob, bilirubin_val, st):
    """
    Muestra una imagen y sus predicciones del modelo en Streamlit.
    """
    imagen = Image.open(fila["ruta"])
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(imagen, caption=os.path.basename(fila["ruta"]), use_container_width=True)

    with col2:
        st.markdown(f"*Etiqueta real:* {fila['etiqueta']}")
        st.markdown(f"*Clase predicha:* {pred_label} ({prob * 100:.1f}%)")
        st.markdown(f"*Bilirrubina predicha:* {bilirubin_val} mg/dL")

        if pred_label == fila["etiqueta"]:
            st.success("✅ La predicción coincide con la etiqueta real.")
        else:
            st.error("❌ La predicción no coincide con la etiqueta real.")