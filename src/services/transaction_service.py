#PROCESAMIENTO DE TRANSACCIONES (transform,load)
"""import pandas as pd
from datetime import datetime
from pathlib import Path
from src.services.file_processor_service import Transaction_Processor  
from src.core.config import EXCEL_FILE_PATH

# Ruta al archivo de prueba
#file_path = Path("data/pruebas/transacciones_prueba.xlsx")
# Cargar y validar archivo usando la instancia importada
df = Transaction_Processor.process_file()

# Transformar columnas específicas
def transform_transaccion(df: pd.DataFrame) -> pd.DataFrame:
    df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True) #le coloque el dayfirst ya que mi excel esta en fomato d/m/a y pandas es m/d/a
    df["Total cobrado"] = df["Total cobrado"].str.replace(r"['\$, ]", '', regex=True)  # Elimina ', $, y espacios
    df["Total cobrado"] = df["Total cobrado"].str.strip()  # Elimina espacios adicionales
    df["Total cobrado"] = pd.to_numeric(df["Total cobrado"], errors='coerce').fillna(0)  # Convierte a float, valores no válidos a 0
    df["Concepto"] = df["Concepto"].str.lower().str.strip()
    df["Promocion"] = df["Promocion"].fillna("Sin promoción")
    return df

df_transformado = transform_transaccion(df)

# Ver info
print("\n📊 Tipos de datos de columnas:")
df_transformado.info()

# Mostrar primeras filas
print("\n🧾 Primeras filas transformadas:") 
print(df_transformado.head(3))"""

import pandas as pd
from datetime import datetime
from pathlib import Path
from src.services.file_processor_service import Transaction_Processor  
from src.core.config import EXCEL_FILE_PATH
import logging

logger= logging.getLogger(__name__)

_df_cache= None

def transform_transaccion(df: pd.DataFrame) -> pd.DataFrame:
    df=df.copy()
    df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True)
    df["Total cobrado"] = df["Total cobrado"].str.replace(r"['\$, ]", '', regex=True)
    df["Total cobrado"] = df["Total cobrado"].str.strip()
    df["Total cobrado"] = pd.to_numeric(df["Total cobrado"], errors='coerce').fillna(0)
    df["Total cobrado"] = df["Total cobrado"].astype(float)
    df["Concepto"] = df["Concepto"].str.lower().str.strip()
    df["Promocion"] = df["Promocion"].fillna("Sin promoción")
    print("\n📊 Tipos de datos de columnas:")
    df.info()
    return df

def obtener_df_transformado() -> pd.DataFrame:
    """Carga y transforma datos con cache"""
    global _df_cache
    
    if _df_cache is not None:
        logger.info("📊 Usando datos cacheados")
        return _df_cache
    
    try:
        logger.info("📂 Cargando datos desde Excel...")
        df = Transaction_Processor.process_file()
        
        if df is None or df.empty:
            raise ValueError("El DataFrame está vacío o es None")
        
        logger.info(f"📊 Datos crudos: {df.shape}")
        
        df = transform_transaccion(df)
        logger.info(f"✅ Datos transformados: {df.shape}")
        
        _df_cache = df
        return df
        
    except Exception as e:
        logger.error(f"❌ Error en obtener_df_transformado: {e}")
        # Retorna DataFrame vacío para evitar errores
        return pd.DataFrame()


