# Importamos las herramientas que construimos en la carpeta 'src'
from src.extraccion import extraer_datos
from src.transformacion import limpiar_datos
from src.carga import guardar_en_bd, guardar_parquet 

def ejecutar_pipeline():
    print("INFO - Arrancando Pipeline Orquestador ETL completo...")
    
    # FASE 1: EXTRACCIÓN
    # Llamamos al módulo que lee el dataset pesado de Kaggle
    ruta_csv = 'datos/Fifa 23 Players Data.csv'
    df_crudo = extraer_datos(ruta_csv)
    
    # FASE 2: TRANSFORMACIÓN
    # Pasamos los datos crudos por el filtro de limpieza
    df_limpio = limpiar_datos(df_crudo)
    
    # FASE 3: CARGA
    # Guardamos los datos procesados en la base de datos y en el archivo de alto rendimiento
    guardar_en_bd(df_limpio, 'jugadores_fifa23_limpio')
    guardar_parquet(df_limpio, 'datos/fifa23_analitica.parquet')
    # FASE 3: CARGA
    # Guardamos los datos procesados en la base de datos y en los archivos de salida
    guardar_en_bd(df_limpio, 'jugadores_fifa23_limpio')
    guardar_parquet(df_limpio, 'datos/fifa23_analitica.parquet')
    
    # NUEVA LÍNEA: Exportar también el resultado limpio a formato CSV para visualizarlo
    df_limpio.to_csv('datos/fifa_sports_cleaned.csv', index=False)
    
    print("INFO - Pipeline ETL completado con éxito. Datos listos.")

# Este bloque asegura que el pipeline solo corra si ejecutamos este archivo directamente
if __name__ == '__main__':
    ejecutar_pipeline()
