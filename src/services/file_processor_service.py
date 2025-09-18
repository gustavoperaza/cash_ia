import pandas as pd
from pathlib import Path
import logging
from src.core.config import EXCEL_FILE_PATH

# Configuración básica del logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class TransactionProcessor:
    TRANSACTION_COLUMNS = ["Fecha", "Concepto", "Medio de Pago", "Aut.",
                           "Total cobrado", "Promocion", "Estado"]

    def __init__(self):
        self.supported_formats = ['.xlsx', '.xls', '.csv']

    def process_file(self, file_path: Path = EXCEL_FILE_PATH) -> pd.DataFrame:

        df = self.load_file(file_path)
        logging.info(f"Archivo '{file_path}' cargado y validado exitosamente.")
        return df

    def load_file(self, file_path: Path) -> pd.DataFrame:
        """Carga archivo Excel o CSV y valida columnas"""
        path = Path(file_path) # cadena que devuelve la ruta especifica del archivo

        if not path.exists():
            raise FileNotFoundError(f"El archivo '{path}' no existe.")
        if path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Formato no soportado: {path.suffix}")

        if path.suffix == '.csv':
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)

        if df.empty:
            raise ValueError("El archivo está vacío.")

        df.columns = df.columns.str.strip()  # Limpia espacios en nombres de columna
        self._validate_columns(df)
        return df

    def _validate_columns(self, df: pd.DataFrame):
        """Valida que el DataFrame contenga las columnas requeridas"""
        missing_columns = [col for col in self.TRANSACTION_COLUMNS if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Faltan las siguientes columnas: {missing_columns}")


# Instancia global para usar en otros módulos
Transaction_Processor = TransactionProcessor() #siempre debo colocarle el () ya que asi puedo acceder a los metodos de la clase
