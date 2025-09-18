from pathlib import Path

# Ruta base del proyecto
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # src/

# Rutas de datos
DATA_DIR = PROJECT_ROOT / "data"
PRUEBAS_DIR = DATA_DIR / "pruebas"
EXCEL_FILE_PATH = PRUEBAS_DIR / "transacciones_prueba.xlsx"