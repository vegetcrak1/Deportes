import pandas as pd
import logging
from src.transformacion import limpiar_datos
from src.carga import cargar_sqlite_idempotente

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def ejecutar_pipeline():
    logging.info("Arrancando Pipeline Orquestador...")
    ruta = 'datos/fifa_sports_raw_data.csv'
    
    # Lectura fraccionada (chunks) y delimitador explicito como manda la guia
    iterador_lotes = pd.read_csv(ruta, sep=',', encoding='utf-8', chunksize=2, low_memory=False)
    
    df_completo = []
    for num, lote in enumerate(iterador_lotes):
        logging.info(f"Procesando lote {num + 1}...")
        lote_limpio = limpiar_datos(lote)
        cargar_sqlite_idempotente(lote_limpio)
        df_completo.append(lote_limpio)
        
    # Exportacion final a Parquet analítico
    if df_completo:
        df_final = pd.concat(df_completo)
        df_final.to_parquet('datos/fifa_analitica.parquet', index=False)
        logging.info("Pipeline completado exitosamente.")

if __name__ == "__main__":
    ejecutar_pipeline()
