import streamlit as st

st.set_page_config(page_title="ℹ️ Acerca del Proyecto", layout="centered")
st.title("ℹ️ Acerca del Proyecto de Diagnóstico de Ictericia Neonatal")

st.markdown("""
Este proyecto forma parte del trabajo de grado titulado:
### 🎓 _"Sistema de diagnóstico no invasivo de ictericia neonatal en Colombia: un enfoque desde la visión por computador"_

---

## 🎯 Objetivo principal
Diseñar una **interfaz gráfica interactiva** en Python que permita cargar imágenes de neonatos y simular el diagnóstico de ictericia, como base para un sistema de apoyo clínico en entornos hospitalarios colombianos.

---

## 🧠 ¿Cómo funciona el sistema?
1. El usuario se autentica con un login seguro.
2. Puede cargar una imagen individual o ejecutar un análisis por lote.
3. El sistema simula la predicción usando un modelo de ML.
4. Los resultados se exportan automáticamente en formato CSV.
5. Un panel tipo dashboard permite visualizar estadísticas agregadas.

---

## 🛠️ Tecnologías utilizadas

| Categoría           | Herramienta                      |
|---------------------|----------------------------------|
| Lenguaje            | Python 3.10+                     |
| Framework UI        | Streamlit                        |
| Procesamiento       | Pillow (PIL), pandas             |
| Visualización       | Streamlit charts, CSV            |
| IDEs                | PyCharm, VSCode                  |
| Dataset             | NeoJaundice (CHD dataset)        |
| Infraestructura     | Local, compatible con Linode     |

---

## 🗂️ Estructura del Proyecto
- 'app.py': Interfaz principal
- 'pages/': Módulos del sistema (Diagnóstico, Dashboard, Análisis por Lote, Acerca de)
- 'core/': Lógica de predicción y carga de datos
- 'utils/': Control de sesión, layout y validaciones
- 'resultados/': CSV de diagnósticos (por lote y acumulado)
- 'NeoJaundice/': Dataset original de imágenes

---

## 👥 Autores del Proyecto
**Angélica María Ruiz** - Ingeniería Biomédica, Pontifica Universidad Javeriana Cali

**Camilo Salazar Barney** - Ingeniería Biomédica, Pontifica Universidad Javeriana Cali

**Director:** Dr. Cristian Alejandro Torres Valencia

---

## 📈 Estado actual del Sistema

| Componente             | Estado        |
|------------------------|---------------|
| Interfaz gráfica       | ✅ Completa    |
| Análisis individual    | ✅ Funcional   |
| Análisis por lote      | ✅ Exporta CSV |
| Dashboard histórico    | ✅ Visual      |
| Login y control        | ✅ Seguro      |
| Conexión a modelo ML   | 🔜 En desarrollo |

---

**Pontificia Universidad Javeriana Cali**  
Facultad de Ingeniería y Ciencias  
Programa: Ingeniería Biomédica  
Año de desarrollo: **2025**

---

### 🔐 Nota de uso
Este sistema ha sido desarrollado con fines **académicos y de demostración**. No cuenta con certificación clínica y **no debe ser utilizado para diagnóstico médico real**.
""")