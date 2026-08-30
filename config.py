# carga las variables de entorno
import os
from dotenv import load_dotenv

load_dotenv()  # lee el archivo .env y carga las variables al entorno

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID")