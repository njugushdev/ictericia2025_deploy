import streamlit as st

st.set_page_config(page_title="ℹ️ Acerca del Sistema", layout="centered")
st.title("ℹ️ Acerca del Sistema de Detección de Ictericia Neonatal")

st.markdown("""
Este sistema web utiliza *modelos de inteligencia artificial* para analizar imágenes de recién nacidos y estimar la presencia de *ictericia neonatal*, una condición frecuente que provoca coloración amarilla en la piel debido al aumento de bilirrubina.

---

## 🧠 ¿Qué hace este sistema?

### ✔️ Diagnóstico individual
El usuario puede cargar una imagen y el sistema:
- Identifica si hay signos de ictericia.
- Muestra la probabilidad del diagnóstico.
- Estima el nivel aproximado de bilirrubina.
- Brinda una interpretación automática del riesgo (leve, moderado o severo).

### ✔️ Análisis por lotes
El usuario puede:
- Analizar varias imágenes del dataset al mismo tiempo.
- Ver ejemplos visuales de predicciones.
- Descargar los resultados en formato CSV.

---

## 🛠️ ¿Cómo funciona?
El sistema utiliza dos modelos de IA entrenados con imágenes reales:

- *Modelo de clasificación:* Detecta ictericia vs no ictericia.  
- *Modelo de regresión:* Estima el nivel de bilirrubina en mg/dL.

Ambos modelos procesan la imagen cargada y generan el diagnóstico final.

---

## 🎯 Propósito
El propósito de esta plataforma es ofrecer una *demostración interactiva* de cómo la visión por computador puede apoyar la detección temprana de ictericia neonatal en entornos clínicos.

Esta interfaz permite visualizar de manera sencilla cómo funcionan los modelos, sus resultados y su posible utilidad en investigaciones futuras.

---

## ⚠️ Advertencia importante
Este sistema tiene *fines educativos y de demostración*.  
No reemplaza una evaluación médica profesional y *no debe ser usado para diagnóstico clínico real*.

---

## 👥 Autores
Proyecto desarrollado como parte de un trabajo académico sobre técnicas de visión por computador aplicadas a la salud neonatal.

""")