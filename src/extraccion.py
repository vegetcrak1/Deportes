import pandas as pd
import numpy as np

def extraer_datos(ruta_archivo):
    print(f"INFO - Iniciando Extracción desde: {ruta_archivo}")
    
    # 1. Leer el archivo CSV
    df = pd.read_csv(ruta_archivo)
    
    # 2. Limpieza preliminar en la extracción: 
    # Convertir los guiones raros "-" en valores nulos oficiales de Python (NaN)
    df.replace('-', np.nan, inplace=True)
    
    print(f"INFO - Extracción completada: {df.shape[0]} registros y {df.shape[1]} columnas obtenidas.")
    return df