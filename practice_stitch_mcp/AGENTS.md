# AGENTS.md — Instrucciones para el agente (OpenCode)

Este repositorio es la plantilla de una actividad en equipo:
1. El equipo diseña **3 o más vistas** de una temática divertida en **Google Stitch**.
2. Tú, el agente, las **extraes con el servidor MCP `stitch`** y las conviertes en código en este repo.
3. El equipo sube los cambios con **Conventional Commits**.

Responde siempre en **español**.

## Herramientas del MCP `stitch`

El servidor ya está configurado en `opencode.json`. En OpenCode sus herramientas llevan el prefijo `stitch_`. Las principales:

| Herramienta | Para qué | Parámetros clave |
|---|---|---|
| `list_projects` | Listar los proyectos del usuario | `filter` (opcional) |
| `get_project` | Detalle de un proyecto | `name` = `projects/{projectId}` |
| `list_screens` | Pantallas de un proyecto | `projectId` |
| `get_screen` | Detalle de una pantalla: HTML, captura | `name` = `projects/{projectId}/screens/{screenId}` |
| `list_design_systems` | Sistema de diseño: colores, tipografía | `projectId` |

**Reglas de uso:**
- **Solo lectura por defecto.** No uses `create_project`, `generate_screen_from_text`, `edit_screens`, `generate_variants` ni las herramientas de design system que crean o modifican nada, salvo que el usuario lo pida explícitamente. Gastan cuota y cambian su trabajo.
- **Nunca** uses `delete_project`.
- **Si una herramienta devuelve un error de autenticación** ("missing required authentication credential", "API keys are not supported", "API key not valid"), significa que la variable de entorno `STITCH_API_KEY` no está definida o no es válida en la terminal donde se abrió OpenCode. Díselo al usuario y remítelo a la sección *Solución de problemas* del README. No intentes arreglarlo tú.
- **El HTML de una pantalla se descarga.** `get_screen` devuelve URLs de descarga (por ejemplo, el HTML y la captura). Descárgalas con `curl -sL "<url>"` o con la herramienta de fetch, y nunca inventes un diseño.

## Flujo para crear una vista

1. `list_projects`: identifica el proyecto del equipo. Si hay varios, pregunta cuál.
2. `list_screens`: muestra la lista de pantallas y confirma con el usuario cuál va en qué vista.
3. `get_screen`: descarga el HTML de la pantalla y míralo junto con la captura.
4. Crea o actualiza el archivo de la vista siguiendo la estructura de abajo. Adapta el HTML de Stitch; no lo pegues sin revisar.
5. Actualiza `index.html` para que enlace todas las vistas.
6. Resume qué archivos cambiaste y **propón** un mensaje de commit convencional. **No hagas `git commit` ni `git push`** a menos que el usuario lo pida.

## Estructura que debes crear (el repo empieza vacío a propósito)

```
index.html            ← portada en la RAÍZ: nombre del equipo, temática y enlaces a cada vista
views/
  <nombre-vista>.html ← una página HTML completa por pantalla de Stitch (kebab-case, p. ej. menu-galactico.html)
  css/                ← (opcional) estilos compartidos, p. ej. views/css/comun.css
  js/                 ← (opcional) scripts clásicos compartidos
  img/                ← (opcional) imágenes descargadas que usen las vistas
docs/
  DESIGN.md           ← (cuando se pida) paleta, tipografía y reglas extraídas del design system de Stitch
README.md             ← ya existe: solo actualiza la sección "Nuestro proyecto" si el usuario lo pide
```

## Convenciones

- **HTML, CSS y JavaScript puros. Sin npm, sin dependencias, sin paso de build.** No crees `package.json`.
- **Se debe poder abrir con doble clic** (`file://`) y también con `npx serve .`:
  - Usa **rutas relativas**: `views/menu.html` desde `index.html`, y `../index.html` desde una vista.
  - **No uses** `<script type="module">`, `import` ni `fetch()` de archivos locales, porque fallan con `file://`. Usa `<script src="...">` clásicos.
  - Si el HTML de Stitch usa Tailwind por CDN (`<script src="https://cdn.tailwindcss.com">` y un `tailwind.config` en línea), puedes conservarlo dentro de esa vista. Es la vía más fiel al diseño. Las fuentes de Google Fonts por `<link>` también son válidas.
- **Cada vista** debe incluir:
  - un `<title>` descriptivo y `<html lang="es">`;
  - `<meta name="viewport" content="width=device-width, initial-scale=1">`;
  - una navegación visible con enlace a `../index.html` y a las demás vistas;
  - contenido de la temática del equipo en español, no *lorem ipsum* si Stitch trae textos.
- **`index.html`** muestra el nombre del equipo, la temática y una tarjeta o enlace por cada archivo de `views/`. Si agregas una vista, agrega su enlace.
- **Accesibilidad básica:** `alt` en las imágenes, contraste legible y botones o enlaces con texto.
- **Imágenes:** si las URLs de Stitch son temporales o requieren sesión, descarga las imágenes a `views/img/` y enlázalas en relativo.
- **Nombres de archivo:** en minúsculas, kebab-case y sin espacios ni tildes.

## Seguridad (obligatorio)

- **La clave de Stitch NUNCA se escribe en ningún archivo.** OpenCode la lee de la variable de entorno del sistema `STITCH_API_KEY` mediante `{env:STITCH_API_KEY}` en `opencode.json`.
- No modifiques el bloque `mcp` de `opencode.json`.
- No imprimas la clave, no la pidas en el chat, no crees `.env` con ella y no la pongas en el código.
- Si el usuario pega una clave en el chat, recuérdale que la rote (que la borre y cree otra en Stitch) y que use la variable de entorno.

## Commits: Conventional Commits

Formato: `tipo(alcance): descripción` (descripción de 5 a 72 caracteres). Ejemplos:
- `feat(views): agrega vista menu-galactico desde Stitch`
- `feat(index): enlaza las tres vistas en la portada`
- `fix(views): corrige rutas de imágenes en reservas`
- `style(views): ajusta espaciado del encabezado`
- `docs(design): documenta paleta y tipografía`

Haz **un commit por vista** cuando sea posible. Si el usuario te pide hacer el commit, usa `git add <archivos concretos>` (nunca `git add -A` a ciegas) y verifica antes que `.env` no esté en el *staging*.
