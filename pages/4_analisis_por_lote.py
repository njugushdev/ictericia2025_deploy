import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import os
import csv
import gdown
from datetime import datetime
from PIL import Image
from utils.layout_utils import verificar_autenticacion
from core.database import cargar_dataset_desde_csv
from core.processor import predict_image, mostrar_imagen_con_prediccion

# ============================================================
# Configuración de la página
# ============================================================
st.set_page_config(
    page_title="Análisis por Lotes - Ictericia Neonatal",
    page_icon="🧪",
    layout="wide"
)

verificar_autenticacion()
st.title("🧪 Análisis por Lotes - Detección de Ictericia Neonatal")

# ============================================================
# Descarga automática del dataset si no existe
# ============================================================
os.makedirs("data", exist_ok=True)
ruta_csv = "data/chd_jaundice_published_2.csv"
ruta_imagenes = "data/images"

# Google Drive file ID (from your link)
file_id = "1LbW-ZuxMHMk04Sk8rE3EwIuACz5QoZvy"
gdrive_url = f"https://drive.google.com/uc?id={file_id}"

if not os.path.exists(ruta_csv):
    with st.spinner("📥 Descargando dataset desde Google Drive..."):
        gdown.download(gdrive_url, ruta_csv, quiet=False)
        st.success("✅ Dataset descargado correctamente.")

# ============================================================
# Cargar dataset (CSV + imágenes)
# ============================================================
try:
    df = cargar_dataset_desde_csv(
        ruta_csv=ruta_csv,
        ruta_imagenes=ruta_imagenes
    )
except Exception as e:
    st.error(f"❌ Error al cargar el dataset: {e}")
    st.stop()

# ============================================================
# Controles de usuario
# ============================================================
cantidad = st.slider("Número de imágenes a analizar", min_value=1, max_value=200, value=10)
mostrar = st.slider("Imágenes a mostrar en pantalla", min_value=1, max_value=min(cantidad, 20), value=5)

# Contadores
aciertos = 0
conteo_ictericia = 0
conteo_no_ictericia = 0
filas = []

# ============================================================
# Bucle principal de análisis por lote
# ============================================================
for i in range(cantidad):
    fila = df.iloc[i]
    image = Image.open(fila["ruta"])

    # Predicción con los modelos reales
    pred_label, prob, bilirubin_val = predict_image(image)

    if pred_label == "ictericia":
        conteo_ictericia += 1
    else:
        conteo_no_ictericia += 1

    match = pred_label == fila["etiqueta"]
    if match:
        aciertos += 1

    # Guardar fila de resultados
    filas.append([
        os.path.basename(fila["ruta"]),
        fila["etiqueta"],
        pred_label,
        prob,
        bilirubin_val,
        "✔️" if match else "❌",
    ])

    # Mostrar imágenes de ejemplo
    if i < mostrar:
        mostrar_imagen_con_prediccion(fila, pred_label, prob, bilirubin_val, st)

# ============================================================
# Guardar resultados
# ============================================================
os.makedirs("resultados", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
archivo_lote = f"resultados/lote_{timestamp}.csv"
archivo_maestro = "resultados/todos_lotes.csv"
columnas = ["imagen", "etiqueta_real", "prediccion", "probabilidad", "bilirrubina_predicha", "acierto"]

# Guardar CSV del lote
with open(archivo_lote, "w", newline="", encoding="utf-8") as f_lote:
    writer = csv.writer(f_lote)
    writer.writerow(columnas)
    writer.writerows(filas)

# ============================================================
# Resumen de resultados
# ============================================================
st.markdown("---")
st.subheader("📈 Resumen de Resultados del Lote")

col1, col2, col3 = st.columns(3)
col1.metric("Total de imágenes", cantidad)
col2.metric("Predicciones correctas", aciertos)
col3.metric("Exactitud", f"{(aciertos / cantidad) * 100:.2f}%")

# Conteo de clases
st.markdown("### 🔍 Conteo de clases predichas")
st.markdown(f"- 🟡 Ictericia: {conteo_ictericia} imágenes")
st.markdown(f"- ⚪ No Ictericia: {conteo_no_ictericia} imágenes")

# Gráfico de barras
df_pred = pd.DataFrame({
    "Clase": ["ictericia", "no_ictericia"],
    "Cantidad": [conteo_ictericia, conteo_no_ictericia]
}).set_index("Clase")
st.bar_chart(df_pred)

st.success(f"✅ Resultados guardados en: {archivo_lote}")