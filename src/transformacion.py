import pandas as pd

def limpiar_datos(df):
    print("INFO - Iniciando Transformación y Limpieza de datos...")
    
    # 1. Eliminar filas que sean copias exactas
    df = df.drop_duplicates().copy()
    
    # 2. Manejo de nulos (los que convertimos en la extracción)
    # Rellenamos los nulos de la columna de préstamos con 'FALSE' y el resto con 'Sin Registro'
    df['On Loan'] = df['On Loan'].fillna('FALSE')
    df.fillna('Sin Registro', inplace=True)
    
    # 3. Filtrado Inteligente: El dataset trae 89 columnas, eso es demasiada basura.
    # Vamos a quedarnos solo con las más importantes para el análisis.
    columnas_clave = [
        'Full Name', 'Age', 'Height(in cm)', 'Weight(in kg)', 
        'Overall', 'Value(in Euro)', 'Club Name', 'Nationality'
    ]
    df_filtrado = df[columnas_clave].copy()
    
    # 4. Asegurar que el dinero y las medidas se traten matemáticamente como números
    df_filtrado['Value(in Euro)'] = pd.to_numeric(df_filtrado['Value(in Euro)'], errors='coerce')
    
    print("INFO - Transformación exitosa. Datos listos para cargar.")
    return df_filtrado
