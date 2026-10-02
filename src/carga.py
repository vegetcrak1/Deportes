import sqlite3
import pandas as pd

def guardar_en_bd(df, nombre_tabla):
    print(f"INFO - Guardando datos en la base de datos SQLite (Tabla: {nombre_tabla})...")
    conexion = sqlite3.connect('datos/almacen_fifa.db')
    df.to_sql(nombre_tabla, conexion, if_exists='replace', index=False)
    conexion.close()
    print("INFO - Datos guardados en SQLite con éxito.")

def guardar_parquet(df, ruta_parquet):
    print(f"INFO - Guardando archivo Parquet de alto rendimiento en: {ruta_parquet}")
    df.to_parquet(ruta_parquet, index=False)
    print("INFO - Archivo Parquet guardado con éxito.")