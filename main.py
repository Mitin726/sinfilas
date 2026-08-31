import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode

from config import TELEGRAM_BOT_TOKEN
from claude_client import interpretar_mensaje
from sheets_client import get_medicamentos, buscar_medicamento
from respuestas import construir_respuesta

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy el bot de disponibilidad de medicamentos 💊\n"
        "Preguntame algo como: '¿tienen ibuprofeno?'"
    )


async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = update.message.text

    # Caso raro: mensaje vacío o solo espacios (raro en Telegram, pero por las dudas)
    if not texto_usuario or not texto_usuario.strip():
        await update.message.reply_text("No recibí ningún texto, intentá de nuevo 🙂")
        return

    logger.info(f"Usuario {update.effective_user.id}: {texto_usuario}")

    try:
        interpretacion = interpretar_mensaje(texto_usuario)
        intent = interpretacion.get("intent", "otro")
        nombre_buscado = interpretacion.get("medicamento")

        encontrado = None
        if intent == "consulta_disponibilidad":
            medicamentos = get_medicamentos()
            encontrado = buscar_medicamento(nombre_buscado, medicamentos)

        respuesta = construir_respuesta(intent, encontrado, nombre_buscado)

    except Exception as e:
        # Cualquier error inesperado (Claude caído, Sheets caído, etc.)
        # no debe tumbar el bot ni dejar al usuario sin respuesta.
        logger.error(f"Error procesando mensaje '{texto_usuario}': {e}")
        respuesta = (
            "Ups, tuve un problema procesando tu mensaje 😕\n"
            "Intentá de nuevo en un momento."
        )

    await update.message.reply_text(respuesta, parse_mode=ParseMode.MARKDOWN)


def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))

    logger.info("Bot iniciado. Esperando mensajes...")
    app.run_polling()


if __name__ == "__main__":
    main()