PROFILE_DATA = {
    "name": "Adonay Navas",
    "career": "Técnico en Ingeniería en Computación",
    "stack": "Java (Spring Boot), Laravel 12, Vue, React, PostgreSQL",
    "phrases": [
        "¡Hola! Soy Adonay Navas.",
        "Estudio Técnico en Ingeniería en Computación.",
        "Me apasiona el desarrollo de software y la arquitectura backend.",
        "Trabajo con Java (Spring Boot), Laravel 12, Vue, React y PostgreSQL.",
        "¡Has completado mi presentación! Sigue jugando para superar tu récord."
    ]
}

def get_presentation_phrase(apples_eaten: int) -> str:
    """Skill: Retorna la frase de presentación correspondiente según las manzanas recolectadas."""
    phrases = PROFILE_DATA["phrases"]
    index = min(apples_eaten, len(phrases) - 1)
    return phrases[index]
