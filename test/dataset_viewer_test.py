import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from core.database import cargar_dataset_desde_csv
from PIL import Image

# Carga del dataset real
df = cargar_dataset_desde_csv(
    ruta_csv="NeoJaundice/chd_jaundice_published_2.csv",
    ruta_imagenes="NeoJaundice/images"
)

st.title("🔬 Visualización de dataset NeoJaundice")

cantidad = st.slider("Cantidad de imágenes a mostrar", 1, 20, 5)

for i in range(cantidad):
    fila = df.iloc[i]
    st.image(Image.open(fila["ruta"]), caption=f"Etiqueta: {fila['etiqueta']}", use_container_width=True)
