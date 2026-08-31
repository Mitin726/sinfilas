# todo lo relacionado a la API de Claude
import json
import logging
from anthropic import Anthropic
from config import ANTHROPIC_API_KEY

logger = logging.getLogger(__name__)

client = Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Eres un clasificador de mensajes para un bot de farmacia.
Tu única tarea es analizar el mensaje del usuario y responder ÚNICAMENTE con un JSON válido, sin texto adicional, sin explicaciones, sin markdown.

Formato exacto de respuesta:
{"intent": "consulta_disponibilidad" | "saludo" | "otro", "medicamento": "<nombre del medicamento o null>"}

Reglas:
- Si el usuario pregunta por disponibilidad, stock, precio o si "tienen" algún medicamento -> intent "consulta_disponibilidad" y extraé el nombre del medicamento (sin la dosis si es posible, en minúsculas).
- Si es un saludo o mensaje de cortesía sin pregunta concreta -> intent "saludo", medicamento null.
- Cualquier otra cosa -> intent "otro", medicamento null.

Responde solo el JSON, nada más."""

def interpretar_mensaje(texto_usuario: str) -> dict:
    """
    Envía el mensaje a Claude y devuelve un diccionario Python
    con 'intent' y 'medicamento'. Si algo falla, devuelve intent 'otro'.
    """
    texto_json = None
    try:
        respuesta = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=100,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": texto_usuario},
                {"role": "assistant", "content": "{"}  # <- prefill: forzamos que empiece con "{"
            ]
        )

        # Como el modelo continúa desde donde le "prefillamos", hay que agregar el "{" de vuelta
        texto_json = "{" + respuesta.content[0].text.strip()
        logger.info(f"Claude respondió: {texto_json}")

        return json.loads(texto_json)

    except json.JSONDecodeError:
        logger.error(f"Claude no devolvió JSON válido: {texto_json}")
        return {"intent": "otro", "medicamento": None}

    except Exception as e:
        logger.error(f"Error llamando a Claude: {e}")
        return {"intent": "otro", "medicamento": None}