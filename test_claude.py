from claude_client import interpretar_mensaje

pruebas = [
    "hola buenas tardes",
    "tienen ibuprofeno de 400?",
    "cuanto cuesta el acetaminofen",
    "gracias, hasta luego"
]

for mensaje in pruebas:
    resultado = interpretar_mensaje(mensaje)
    print(f"'{mensaje}' -> {resultado}")