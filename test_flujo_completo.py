from claude_client import interpretar_mensaje
from sheets_client import get_medicamentos, buscar_medicamento
from respuestas import construir_respuesta

medicamentos = get_medicamentos()  # traemos la data una sola vez

pruebas = [
    "hola buenas tardes",
    "tienen ibuprofeno?",
    "cuanto cuesta el acetaminofen",
    "hay loratadina disponible",
    "gracias, hasta luego"
]

for mensaje in pruebas:
    interpretacion = interpretar_mensaje(mensaje)
    intent = interpretacion["intent"]
    nombre_buscado = interpretacion["medicamento"]

    encontrado = None
    if intent == "consulta_disponibilidad":
        encontrado = buscar_medicamento(nombre_buscado, medicamentos)

    respuesta = construir_respuesta(intent, encontrado, nombre_buscado)

    print(f"\n👤 Usuario: {mensaje}")
    print(f"🔍 Interpretación: {interpretacion}")
    print(f"🤖 Bot: {respuesta}")