# agent.py
from skills.presentation_skill import get_presentation_phrase
from skills.feedback_skill import get_game_over_feedback

class PresentationAgent:
    """
    Agente encargado de coordinar y ejecutar las Skills
    según los eventos y el estado del juego.
    """
    def __init__(self):
        self.name = "Agente de Presentación de Adonay"

    def get_current_phrase(self, score: int) -> str:
        """Invoca la skill para obtener la frase de presentación actual."""
        return get_presentation_phrase(score)

    def evaluate_performance(self, score: int) -> str:
        """Invoca la skill para obtener la retroalimentación de final de juego."""
        return get_game_over_feedback(score)
