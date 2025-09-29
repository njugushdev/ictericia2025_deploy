import pandas as pd
import os

def cargar_dataset_desde_csv(ruta_csv: str, ruta_imagenes: str) -> pd.DataFrame:
    df = pd.read_csv(ruta_csv)

    if 'image_idx' not in df.columns or 'blood(mg/dL)' not in df.columns:
        raise ValueError("CSV debe contener 'image_idx' y 'blood(mg/dL)'.")

    # Ruta de cada imagen
    df['ruta'] = df['image_idx'].astype(str).apply(lambda x: os.path.join(ruta_imagenes, x))

    # Etiqueta según nivel de bilirrubina (ajustable)
    df['etiqueta'] = df['blood(mg/dL)'].apply(lambda x: 'ictericia' if x >= 12.0 else 'no_ictericia')

    return df[['ruta', 'etiqueta']].sample(frac=1).reset_index(drop=True)