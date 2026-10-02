# Pipeline ETL: Procesamiento de Datos Deportivos (FIFA)

Este proyecto implementa una arquitectura ETL (Extracción, Transformación y Carga) modular para el procesamiento eficiente de datos deportivos, cumpliendo con estándares de ingeniería de datos y manejo seguro de memoria.

## Arquitectura del Proyecto

El repositorio sigue una separación estricta de responsabilidades:

- `main.py`: Script orquestador del pipeline. Controla el flujo de ejecución.
- `src/transformacion.py`: Módulo responsable de la limpieza, casteos de tipos y normalización de cadenas.
- `src/carga.py`: Módulo encargado de la conexión a la base de datos y la carga idempotente.
- `datos/`: Directorio local (ignorado en el control de versiones) para almacenamiento de inputs y outputs.

## Características Técnicas Implementadas

1. **Lectura Defensiva (Chunking):** Los datos se extraen utilizando particionado por lotes (`chunksize`) mediante Pandas, evitando desbordamientos de memoria (OOM) en conjuntos de datos masivos.
2. **Carga Idempotente:** Inserción en SQLite (`almacen_fifa.db`) validando la preexistencia de IDs, garantizando que el pipeline pueda ejecutarse múltiples veces sin duplicar registros.
3. **Almacenamiento Analítico:** Exportación final a formato columnar `.parquet` (`fifa_analitica.parquet`), optimizado para consultas OLAP y compresión de datos.

## Ejecución del Pipeline

Para reproducir el entorno y ejecutar el pipeline:

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt