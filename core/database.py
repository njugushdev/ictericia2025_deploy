import pandas as pd
import os

def cargar_dataset_desde_csv(ruta_csv: str, ruta_imagenes: str) -> pd.DataFrame:
    """
    Carga el conjunto de datos desde un archivo CSV y crea un DataFrame
    con las rutas de las imágenes y sus etiquetas.

    Parámetros:
        ruta_csv: Ruta del archivo CSV que contiene las columnas ['image_idx', 'blood(mg/dL)'].
        ruta_imagenes: Directorio donde se almacenan las imágenes.

    Retorna:
        DataFrame con las columnas ['ruta', 'etiqueta'].
    """
    df = pd.read_csv(ruta_csv)

    if 'image_idx' not in df.columns or 'blood(mg/dL)' not in df.columns:
        raise ValueError("El CSV debe contener las columnas 'image_idx' y 'blood(mg/dL)'.")

    # Agregar la ruta completa de cada imagen
    df['ruta'] = df['image_idx'].astype(str).apply(lambda x: os.path.join(ruta_imagenes, x))

    # Asignar etiqueta automáticamente: ictericia si bilirrubina >= 12 mg/dL
    df['etiqueta'] = df['blood(mg/dL)'].apply(lambda x: 'ictericia' if x >= 12.0 else 'no_ictericia')

    # Mezclar aleatoriamente las filas
    return df[['ruta', 'etiqueta']].sample(frac=1).reset_index(drop=True)