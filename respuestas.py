def construir_respuesta(intent: str, medicamento_encontrado: dict | None, nombre_buscado: str | None) -> str:
    """
    Arma la respuesta final para el usuario según el intent y los datos
    encontrados en Sheets. NO llama a la API de Claude, todo es texto plantilla.
    """
    if intent == "saludo":
        return (
            "¡Hola! 👋 Soy el bot de disponibilidad de medicamentos.\n"
            "Preguntame algo como: '¿tienen ibuprofeno?' o 'cuánto cuesta el acetaminofén'."
        )

    if intent == "consulta_disponibilidad":
        if medicamento_encontrado is None:
            return (
                f"No encontré '{nombre_buscado}' en nuestra base de datos. 😕\n"
                "Verificá el nombre o probá con otro medicamento."
            )

        stock = medicamento_encontrado.get("stock", 0)
        nombre = medicamento_encontrado.get("nombre", "")
        presentacion = medicamento_encontrado.get("presentacion", "")
        precio = medicamento_encontrado.get("precio", "")
        laboratorio = medicamento_encontrado.get("laboratorio", "")

        if int(stock) > 0:
            return (
                f"✅ Sí, tenemos *{nombre}* disponible.\n"
                f"📦 Presentación: {presentacion}\n"
                f"💰 Precio: ${precio}\n"
                f"🏭 Laboratorio: {laboratorio}\n"
                f"📊 Unidades en stock: {stock}"
            )
        else:
            return (
                f"❌ *{nombre}* está agotado en este momento.\n"
                "Te recomendamos consultar más tarde o preguntar por una alternativa."
            )

    # intent == "otro"
    return (
        "No entendí bien tu mensaje 🤔\n"
        "Podés preguntarme por la disponibilidad de un medicamento, "
        "por ejemplo: '¿tienen loratadina?'"
    )