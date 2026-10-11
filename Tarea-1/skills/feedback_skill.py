def get_game_over_feedback(apples_eaten: int) -> str:
    """Skill: Evalúa la puntuación del jugador y genera una retroalimentación personalizada."""
    if apples_eaten == 0:
        return "¡Ánimo! Intenta recolectar al menos una manzana en la próxima ronda."
    elif apples_eaten < 3:
        return "¡Buen intento! Vas tomando el ritmo del juego."
    elif apples_eaten < 5:
        return "¡Excelente partida! Conociste gran parte de mi perfil profesional."
    else:
        return "¡Impresionante! Has demostrado un gran dominio y completado la presentación."
