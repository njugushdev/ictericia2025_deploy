import streamlit as st
import pandas as pd
import os
import csv
from datetime import datetime
from PIL import Image
from utils.layout_utils import verificar_autenticacion
from core.database import cargar_dataset_desde_csv
from core.processor import predecir_con_modelo_falso, mostrar_imagen_con_prediccion

st.set_page_config(
    page_title = "Análisis por Lote",
    page_icon = "🧪",
    layout = "wide"
)

verificar_autenticacion()

st.title("🧪 Análisis simulado por Lote")

# Cargar dataset real (CSV + imágenes)
df = cargar_dataset_desde_csv(
    ruta_csv="NeoJaundice/chd_jaundice_published_2.csv",
    ruta_imagenes="NeoJaundice/images"
)

# Sliders de control
cantidad = st.slider("Cantidad de imágenes a analizar", min_value=1, max_value=200, value=10)
mostrar = st.slider("Imágenes a mostrar en pantalla", min_value=1, max_value=min(cantidad, 20), value=5)

#Inicializar resultados
aciertos = 0
conteo_ictericia = 0
conteo_no_ictericia = 0
filas = []

# Bucle principal de análisis
for i in range(cantidad):
    fila = df.iloc[i]
    imagen = Image.open(fila["ruta"])
    pred, prob = predecir_con_modelo_falso(imagen)

    if pred == "ictericia":
        conteo_ictericia += 1
    else:
        conteo_no_ictericia += 1
    match = pred == fila["etiqueta"]
    if match:
        aciertos += 1

    #Exportar fila
    filas.append([
        os.path.basename(fila["ruta"]),
        fila["etiqueta"],
        pred,
        prob,
        "✔️" if match else "❌",
    ])

    # Mostrar imagen en pantalla (solo algunas)
    if i < mostrar:
        mostrar_imagen_con_prediccion(fila, pred, prob, st)

# Exportar resultados
os.makedirs("resultados", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
archivo_lote = f"resultados/lote_{timestamp}.csv"
archivo_maestro = "resultados/todos_lotes.csv"
columnas = ["imagen", "etiqueta_real", "prediccion", "probabilidad", "acierto"]

# Guardar CSV del lote
with open(archivo_lote, "w", newline="", encoding="utf-8") as f_lote:
    writer = csv.writer(f_lote)
    writer.writerow(columnas)
    writer.writerows(filas)

# Mostrar resultados del lote
st.markdown("---")
st.subheader("📈 Resultado de lote analizado")
col1, col2, col3 = st.columns(3)
col1.metric("Total imágenes", cantidad)
col2.metric("Aciertos", aciertos)
col3.metric("Exactitud simulada", f"{(aciertos / cantidad) * 100:.2f}%")

# Conteo por clase
st.markdown("### 🔍 Predicciones realizadas")
st.markdown(f"- 🟡 Ictericia: '{conteo_ictericia}' imágenes")
st.markdown(f"- ⚪ No Ictericia: '{conteo_no_ictericia}' imágenes")

# Gráfico
df_pred = pd.DataFrame({
    "Clase": ["ictericia", "no_ictericia"],
    "Cantidad": [conteo_ictericia, conteo_no_ictericia]
})
st.markdown("### 📊 Distribución de clases predichas")
st.bar_chart(df_pred["Clase"])