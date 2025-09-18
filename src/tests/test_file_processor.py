import pytest
from pathlib import Path
import pandas as pd
from core.config import EXCEL_FILE_PATH
from services.file_processor_service import TransactionProcessor  #Importamos la clase de file_processor_service
import logging

# Fixtures para pruebas
@pytest.fixture
def processor(): #creamos una instancia limpia de TransactionProcessor para cada prueba
    return TransactionProcessor()

@pytest.fixture
def sample_data(): # es un DF de ejemplo con datos validos
    return pd.DataFrame({
        "Fecha": ["2023-01-01"],
        "Concepto": ["Venta"],
        "Medio de Pago": ["Efectivo"],
        "Aut.": [None],
        "Total cobrado": [100.0],
        "Promocion": [None],
        "Estado": ["Aprobado"]
    })

@pytest.fixture
def temp_excel_file(tmp_path, sample_data): #achivos temporal para pruebas en xlsx mandandole 2 parametros 
    file_path = tmp_path / "test.xlsx" # este es una fixture propia de pytest que devuelve un objeto pathlib.path que apunta a un directorio temporal y que se concatena con el nombre del archivo usando el operador / de pathlib
    sample_data.to_excel(file_path, index=False) #agarramos el DF  de sample data y lo exportamos a excel en la ruta de file_path y le decimos que no guarde los indices de las filas como una columna más.
    return file_path # devolvemos la ruta ruta absoluta del archivo excel temporal para que otros test lo puedan usar cuando declaren como parametro temp_excel_file

@pytest.fixture
def temp_csv_file(tmp_path, sample_data): #archivos temporales para pruebas en csv
    file_path = tmp_path / "test.csv"
    sample_data.to_csv(file_path, index=False)
    return file_path

@pytest.fixture
def empty_excel_file(tmp_path):  #verificar que el archivo no este vacio
    file_path = tmp_path / "empty.xlsx"
    pd.DataFrame().to_excel(file_path) # crea un DF vacio y se exportara a excel en la ruta de file_path
    return file_path # retornamos la ruta absoluta del excel vacio a empty_excel_file

#PRUEBAS UNITARIAS

class TestTransactionProcessor: #verificar que se pueda cargar un archivo excel valido
    def test_load_valid_excel(self, processor, temp_excel_file):
        """Test que carga un archivo Excel válido"""
        df = processor.load_file(temp_excel_file)
        assert not df.empty 
        assert list(df.columns) == TransactionProcessor.TRANSACTION_COLUMNS

    def test_load_valid_csv(self, processor, temp_csv_file): #verificar que se pueda cargar un csv
        """Test que carga un archivo CSV válido"""
        df = processor.load_file(temp_csv_file)
        assert not df.empty
        assert list(df.columns) == TransactionProcessor.TRANSACTION_COLUMNS

    def test_load_nonexistent_file(self, processor):  #este test verifica el manejo de archivos no existentes
        """Test para archivo que no existe"""
        with pytest.raises(FileNotFoundError): #practicamente le dice a pytest que dentro de este bloque se espera que lance la excepcion file not found
            processor.load_file(Path("no_existe.xlsx"))

    def test_load_unsupported_format(self, processor, tmp_path): # verifica el manejo de formatos no soportados
        """Test para formato no soportado"""
        file_path = tmp_path / "test.txt"
        file_path.touch()
        # el pytest.raises siempre vendra acompañado de un with 
        with pytest.raises(ValueError) as excinfo: #
            processor.load_file(file_path)
        assert "Formato no soportado" in str(excinfo.value)

    def test_load_empty_file(self, processor, empty_excel_file): #verifica el manejo de archivos vacios
        """Test para archivo vacío"""
        with pytest.raises(ValueError) as excinfo:
            processor.load_file(empty_excel_file)
        assert "El archivo está vacío" in str(excinfo.value)

    def test_missing_columns(self, processor, tmp_path, sample_data): #verifica la validacion de columnas faltantes
        """Test para columnas faltantes"""
        # Crear dataframe con columnas faltantes
        bad_data = sample_data.drop(columns=["Fecha", "Concepto"])
        file_path = tmp_path / "bad_columns.xlsx"
        bad_data.to_excel(file_path, index=False)
        
        with pytest.raises(ValueError) as excinfo:
            processor.load_file(file_path)
        assert "Faltan las siguientes columnas" in str(excinfo.value)
        assert "Fecha" in str(excinfo.value)
        assert "Concepto" in str(excinfo.value)

def test_process_file_success(processor, mocker):
    """Test para el método process_file"""
    mock_df = pd.DataFrame(columns=TransactionProcessor.TRANSACTION_COLUMNS)
    mocker.patch.object(processor, 'load_file', return_value=mock_df)

    result = processor.process_file("dummy_path.xlsx")

    processor.load_file.assert_called_once_with("dummy_path.xlsx")
    assert result.equals(mock_df)


