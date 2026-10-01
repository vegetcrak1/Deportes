import pandas as pd
import re
import logging
import time
from sqlalchemy import create_engine, text

# Configuracion pa ver los logs bonitos en la terminal
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def generar_dataset_sucio():
    # Creamos el archivo crudo con errores pa simular la extraccion real
    datos = {
        'ID': [101, 102, 102, 103, 104, 999], # Ojo, el 102 esta duplicado
        'Name': ['Lionel Messi\n', 'C. Ronaldo ', 'C. Ronaldo ', 'Neymar Jr', 'K. Mbappe', 'ERROR_PLAYER'],
        'Value': ['€103.5M', '€90M', '€90M', '€560K', '€120.5M', '€0'],
        'Height': ["5'7", "6'2", "6'2", "5'9", "5'10", "0'0"],
        'Weight': ['159lbs', '183lbs', '183lbs', '150lbs', '160lbs', '0lbs'],
        'Rating': ['93 W/F', '92 W/F', '92 W/F', '91', '91 W/F', 'ERROR']
    }
    df_sucio = pd.DataFrame(datos)
    df_sucio.to_csv('fifa_sports_raw_data.csv', index=False)
    logging.info("1. Archivo fifa_sports_raw_data.csv generado con errores a proposito.")

# --- FUNCIONES DE LIMPIEZA ---

def parsear_plata(valor):
    if pd.isna(valor) or valor == 'ERROR': 
        return 0.0
    val_str = str(valor).replace('€', '').strip()
    if 'M' in val_str:
        return float(val_str.replace('M', '')) * 1000000
    elif 'K' in val_str:
        return float(val_str.replace('K', '')) * 1000
    return float(val_str)

def convertir_altura_cm(altura):
    try:
        partes = str(altura).split("'")
        pies = float(partes[0])
        pulgadas = float(partes[1]) if len(partes) > 1 and partes[1].strip() != "" else 0
        return round((pies * 30.48) + (pulgadas * 2.54), 2)
    except:
        return None

def convertir_peso_kg(peso):
    try:
        # puro regex pa sacar solo los numeros
        num = re.sub(r'[^\d.]', '', str(peso))
        return round(float(num) * 0.453592, 2)
    except:
        return None

def limpiar_rating(rating):
    # quitamos ese ' W/F' raro de los ratings
    if pd.isna(rating): return None
    limpio = re.sub(r'\s*W/F\s*', '', str(rating))
    return int(limpio) if limpio.isdigit() else None

# --- PIPELINE PRINCIPAL ---

def ejecutar_pipeline():
    generar_dataset_sucio()
    
    logging.info("2. Arrancando lectura y limpieza (Transformacion)...")
    df = pd.read_csv('fifa_sports_raw_data.csv')
    
    # a. Deduplicacion logica
    df = df.drop_duplicates(subset=['ID'], keep='first')
    
    # b. Limpiar cadenas (quitar \n y espacios extra)
    df['Name'] = df['Name'].str.strip()
    
    # c. Filtrar basura
    df = df[df['Name'] != 'ERROR_PLAYER']
    df = df[df['Rating'] != 'ERROR']
    
    # d. Parseos y conversiones
    df['Value_EUR'] = df['Value'].apply(parsear_plata)
    df['Height_CM'] = df['Height'].apply(convertir_altura_cm)
    df['Weight_KG'] = df['Weight'].apply(convertir_peso_kg)
    df['Rating_Clean'] = df['Rating'].apply(limpiar_rating)
    
    # Botamos las columnas viejas pa dejar solo lo limpio
    df_limpio = df[['ID', 'Name', 'Value_EUR', 'Height_CM', 'Weight_KG', 'Rating_Clean']]
    
    # Exportamos un csv limpio por si las moscas
    df_limpio.to_csv('fifa_sports_cleaned.csv', index=False)
    logging.info(f"3. Limpieza terminada. Quedaron {len(df_limpio)} jugadores melos.")
    
    # --- CARGA IDEMPOTENTE Y DUAL (SQL + PARQUET) ---
    logging.info("4. Iniciando carga a base de datos...")
    motor_bd = create_engine('sqlite:///almacen_fifa.db')
    
    with motor_bd.connect() as conexion:
        # Revisamos q IDs ya existen pa no meter repetidos
        try:
            resultado = pd.read_sql(text("SELECT ID FROM jugadores_dim"), con=conexion)
            ids_existentes = resultado['ID'].tolist()
        except:
            # si la tabla no existe, la lista arranca vacia
            ids_existentes = []
            
        df_nuevos = df_limpio[~df_limpio['ID'].isin(ids_existentes)]
        
        if not df_nuevos.empty:
            df_nuevos.to_sql('jugadores_dim', con=motor_bd, if_exists='append', index=False)
            logging.info(f"-> Se cargaron {len(df_nuevos)} registros nuevos de forma idempotente.")
        else:
            logging.info("-> No hay datos nuevos pa cargar. Todo actualizado.")
            
    # Exportacion a parquet (Bulk analitico)
    df_limpio.to_parquet('fifa_analitica.parquet', index=False)
    logging.info("5. Exportacion a Parquet completada. Pipeline finalizado con exito.")

if __name__ == '__main__':
    ejecutar_pipeline()