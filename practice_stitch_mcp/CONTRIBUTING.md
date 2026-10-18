# Cómo trabajamos (roles y flujo del equipo)

## Roles sugeridos (equipos de 3 a 5 personas; los roles se pueden combinar)

| Rol | Responsabilidad |
|---|---|
| **Líder / integrador(a)** | Crea el repo desde la plantilla, invita al equipo, protege `main` (opcional) y resuelve conflictos. |
| **Diseñador(a) Stitch** | Define la temática y diseña las 3 o más pantallas en Stitch, con un estilo coherente. Comparte el proyecto de Stitch con el equipo si hace falta. |
| **Operador(a) del agente** | Conduce OpenCode: importa cada pantalla a `views/` y revisa que el resultado se parezca al diseño. |
| **QA / revisor(a)** | Abre el sitio (doble clic o `npx serve .`), prueba enlaces, móvil y accesibilidad, y reporta los arreglos. |
| **Guardián(a) de commits** | Cuida que cada commit siga Conventional Commits, que `.env` y las claves no se suban y que el historial cuente la historia. |

## Flujo recomendado (1 hora)

| Minuto | Qué |
|---|---|
| 0–10 | Crear el repo desde la plantilla, invitar al equipo, clonar y configurar `STITCH_API_KEY` |
| 10–25 | Diseñar las 3 o más vistas en Stitch |
| 25–45 | Importar las vistas con OpenCode + Stitch MCP (una por persona o en paralelo por ramas) |
| 45–55 | Revisión: enlaces, `index.html`, ajustes visuales |
| 55–60 | Último push y demo al grupo |

## Ramas y commits

- **Opción simple:** todos commitean a `main` haciendo antes `git pull --rebase`.
- **Opción recomendada:** una rama por vista (`feat/vista-menu`) y Pull Request a `main`.
- **Un commit por cambio lógico.** Los mensajes siguen *Conventional Commits* (ver la tabla en el README).
- Activa el hook opcional que valida los mensajes: `git config core.hooksPath .githooks`.

## Lo que NUNCA se sube

`.env`, claves de API (incluida la de Stitch) y `node_modules/`. Si alguien sube una clave por error, hay que **borrarla en Stitch y crear otra**: borrarla del repo no basta, porque queda en el historial.
