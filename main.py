# punto de entrada del bot
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import TELEGRAM_BOT_TOKEN

# Configurar logs básicos para ver qué está pasando en la consola
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Se ejecuta cuando el usuario envía /start"""
    await update.message.reply_text(
        "¡Hola! Soy Alba, tu bot de disponibilidad de medicamentos 💊\n"
        "Preguntame algo como: '¿tienen ibuprofeno?'"
    )


async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Se ejecuta con cualquier mensaje de texto que NO sea un comando"""
    texto_usuario = update.message.text
    logger.info(f"Mensaje recibido: {texto_usuario}")

    # Por ahora, un eco simple.
    await update.message.reply_text(f"Recibí tu mensaje: {texto_usuario}")


def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Registrar handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))

    logger.info("Bot iniciado. Esperando mensajes...")
    app.run_polling()


if __name__ == "__main__":
    main()