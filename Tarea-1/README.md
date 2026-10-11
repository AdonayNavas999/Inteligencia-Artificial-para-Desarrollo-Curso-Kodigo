# 🐍 Snake con Sistema Agéntico — Tarea 1

---

## 📌 Descripción del Proyecto

Juego Snake desarrollado en Python con Pygame, refactorizado para incorporar un **sistema agéntico modular** basado en Skills personalizadas. El agente coordina el comportamiento del juego mostrando frases dinámicas del perfil profesional del autor y retroalimentación personalizada al finalizar cada partida.

---

## 🧠 Arquitectura del Sistema Agéntico

```
main.py
  └── run_game() [game.py]
        └── PresentationAgent [agent.py]
              ├── get_current_phrase()   →  presentation_skill.py
              └── evaluate_performance() →  feedback_skill.py
```

---

## ⚙️ Instalación y ejecución

### Requisitos
- Python 3.8+
- pygame

### Instalar dependencias
```bash
pip install pygame
```

### Ejecutar el juego
```bash
python main.py
```

---

## 🔗 Repositorio

[Ver proyecto en GitHub](https://github.com/AdonayNavas999/Inteligencia-Artificial-para-Desarrollo-Curso-Kodigo/tree/4fe39ce00cb843adde73428f63c05a57e167aa3e/Tarea-1)
