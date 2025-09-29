import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.layout_utils import verificar_autenticacion


st.set_page_config(
    page_title = "Dashboard - Ictericia Neonatal",
    page_icon = "📊",
    layout = "wide"
)

verificar_autenticacion()

st.title("📊 Dashboard de Diagnósticos - Ictericia Neonatal")

# Ruta del CSV acumulado
csv_path = "resultados/todos_lotes.csv"

if not os.path.exists(csv_path):
    st.warning("No se ha encontrado el archivo de resultados acumulado (todos_lotes.csv). Asegúrese de haber realizado al menos un análisis.")
    st.stop()

# Cargar datos
with st.spinner("🔄 Cargando datos..."):
    df = pd.read_csv(csv_path)

# Validar estructura
columnas_esperadas = {"imagen," "etiqueta_real", "prediccion", "probabilidad", "acierto"}
if not columnas_esperadas.issubset(df.columns):
    st.error("El archivo no contiene las columnas necesarias.")
    st.stop()

# Mostrar tabla completa (opcional)
with st.expander("🔍 Ver tabla completa"):
    st.dataframe(df)

# Métricas globales
total = len(df)
ictericia = df.loc[df["prediccion"] == "ictericia"].shape[0]
no_ictericia = df.loc[df["prediccion"] == "no_ictericia"].shape[0]
aciertos = df.loc[df["acierto"] == "✔️"].shape[0]
errores = df.loc[df["acierto"] == "❌"].shape[0]
exactitud = (aciertos / total) * 100 if total else 0


col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de imágenes analizadas", total)
col2.metric("Predicciones: Ictericia", ictericia)
col3.metric("Predicciones: No Ictericia", no_ictericia)
col4.metric("Exactitud Global", f"{exactitud:.2f}%")

# Gráficos
st.markdown("---")
st.subheader("📊 Distribución por Clase")
st.bar_chart(pd.DataFrame({
    "Clase": ["ictericia", "no_ictericia"],
    "Cantidad": [ictericia, no_ictericia]
}).set_index("Clase"))

st.subheader("✅ Aciertos vs ❌Errores")
st.bar_chart(pd.DataFrame({
    "Resultado": ["Aciertos", "Errores"],
    "Cantidad": [aciertos, errores]
}).set_index("Resultado"))

# Última actualización
st.markdown("---")
st.caption(f"🕒 Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
