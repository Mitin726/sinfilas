# todo lo relacionado a Google Sheets
import gspread
from google.oauth2.service_account import Credentials
from config import GOOGLE_SHEETS_ID
from rapidfuzz import fuzz, process
import logging

logger = logging.getLogger(__name__)

# Los "scopes" son los permisos que le pedimos a Google.
# Necesitamos leer/escribir Sheets, y Drive para que pueda ubicar el archivo.
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def get_sheet():
    """Devuelve la primera hoja (worksheet) del spreadsheet configurado."""
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(GOOGLE_SHEETS_ID)
    return spreadsheet.sheet1  # la primera pestaña/hoja

def get_medicamentos():
    """
    Trae todos los datos como una lista de diccionarios,
    usando la primera fila como claves (headers).
    """
    sheet = get_sheet()
    registros = sheet.get_all_records()
    return registros

def buscar_medicamento(nombre_buscado: str, medicamentos: list, umbral: int = 60):
    """
    Busca el medicamento más parecido al nombre dado, usando fuzzy matching.
    Devuelve el diccionario del medicamento encontrado, o None si no hay
    ninguno lo suficientemente parecido (según el umbral, 0-100).
    """
    if not nombre_buscado or not medicamentos:
        return None

    nombres = [m["nombre"] for m in medicamentos]

    # process.extractOne busca el mejor match y dice qué tan parecido es (score 0-100)
    resultado = process.extractOne(
        nombre_buscado,
        nombres,
        scorer=fuzz.partial_ratio  # compara aunque el string buscado sea más corto/incompleto
    )

    if resultado is None:
        return None

    nombre_encontrado, score, indice = resultado
    logger.info(f"Búsqueda '{nombre_buscado}' -> '{nombre_encontrado}' (score: {score})")

    if score < umbral:
        return None

    return medicamentos[indice]