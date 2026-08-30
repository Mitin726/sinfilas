# todo lo relacionado a Google Sheets
import gspread
from google.oauth2.service_account import Credentials
from config import GOOGLE_SHEETS_ID

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