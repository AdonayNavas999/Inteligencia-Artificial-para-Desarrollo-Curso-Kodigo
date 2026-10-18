---
description: Importa una pantalla de Stitch como vista HTML en views/
---

Usa el servidor MCP `stitch` siguiendo AGENTS.md (solo herramientas de lectura).

1. Busca en mis proyectos de Stitch la pantalla que coincida con: "$ARGUMENTS". Si hay varias candidatas o dudas, muéstrame la lista y pregúntame.
2. Descarga su HTML con get_screen y conviértelo en `views/<nombre-en-kebab-case>.html`, respetando las convenciones de AGENTS.md (HTML/CSS/JS puros, rutas relativas, navegación a ../index.html y a las demás vistas, y que funcione con doble clic).
3. Crea o actualiza `index.html` en la raíz para que enlace todas las vistas.
4. Dime qué archivos cambiaste y propón un mensaje de commit convencional. No hagas commit.
