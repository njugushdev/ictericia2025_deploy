# Importaciones y carga del dataset
import sys
import pandas as pd
import csv
from datetime import datetime
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.processor import mostrar_imagen_con_prediccion
from PIL import Image
import streamlit as st
from core.database import cargar_dataset_desde_csv
from core.processor import predecir_con_modelo_falso


st.set_page_config(layout="wide")
st.title("🤖 Prueba con Predicciones Simuladas")

# Cargar dataset real
df = cargar_dataset_desde_csv(
    ruta_csv="NeoJaundice/chd_jaundice_published_2.csv",
    ruta_imagenes="NeoJaundice/images"
)
# Sliders: cantidad y visualización en Streamlit
cantidad = st.slider("Cantidad de imágenes a analizar", 1, 200, 10)
mostrar = st.slider("Cantidad de imágenes a mostrar en pantalla", 1, min(cantidad, 20), 5)
filas = []

aciertos = 0
conteo_ictericia = 0
conteo_no_ictericia = 0


#Bucle principal de Análisis
for i in range(cantidad):
    fila = df.iloc[i]
    imagen = Image.open(fila["ruta"])
    pred, prob = predecir_con_modelo_falso(imagen)
    if pred == "ictericia":
        conteo_ictericia += 1
    else:
        conteo_no_ictericia += 1
    match = pred == fila["etiqueta"]

    # Exportar esta fila
    filas.append([
        os.path.basename(fila["ruta"]),
        fila["etiqueta"],
        pred,
        prob,
        "✔️" if match else "❌"
    ])

    if i < mostrar:
        mostrar_imagen_con_prediccion(fila, pred, prob, st)

    if match:
        aciertos += 1

# Crear carpeta si no existe
os.makedirs("resultados", exist_ok=True)

# Nombres de archivos
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
archivo_lote = f"resultados/lote_{timestamp}.csv"
archivo_maestro = "resultados/todos_lotes.csv"
columnas = ["imagen", "etiqueta_real", "prediccion", "probabilidad", "acierto"]

# Exportar CSV del lote actual
with open(archivo_lote, mode="w", newline="", encoding="utf-8") as f_lote:
    writer = csv.writer(f_lote)
    writer.writerow(columnas)
    writer.writerows(filas)

# Exportar al CSV acumulado
nuevo_archivo = not os.path.exists(archivo_maestro)
with open(archivo_maestro, mode="a", newline="", encoding="utf-8") as f_master:
    writer = csv.writer(f_master)
    if nuevo_archivo:
        writer.writerow(columnas)
    writer.writerows(filas)


st.markdown("---")
st.subheader("📈 Resultados del lote analizado")
# Métricas principales
col1, col2, col3 = st.columns(3)
col1.metric("Total imágenes", cantidad)
col2.metric("Aciertos", aciertos)
col3.metric("Exactitud simulada", f"{(aciertos / cantidad) * 100:.2f}%")

# Conteo por clase
st.markdown("### 🔍 Predicciones realizadas")
st.markdown(f"- 🟡 Ictericia: `{conteo_ictericia}` imágenes")
st.markdown(f"- ⚪ No Ictericia: `{conteo_no_ictericia}` imágenes")

# Gráfico de distribución de clases
df_pred = pd.DataFrame({
    "Clase": ["ictericia", "no_ictericia"],
    "Cantidad": [conteo_ictericia, conteo_no_ictericia]
})
# Gráfico dentro de una columna para que no ocupe todo el ancho
col4, col5 = st.columns([1, 2])
with col5:
    st.markdown("### 📊 Distribución de clases predichas")
    st.bar_chart(df_pred.set_index("Clase"))

