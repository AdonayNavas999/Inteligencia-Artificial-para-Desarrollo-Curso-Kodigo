import pygame
import random
import sys

# Inicializar Pygame
pygame.init()
pygame.font.init()

# Configuración de la pantalla y el área de juego
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700  # 600px de área jugable + 100px de banner superior
BANNER_HEIGHT = 100
GAME_HEIGHT = WINDOW_HEIGHT - BANNER_HEIGHT
GRID_SIZE = 20

# Colores (RGB / RGBA)
COLOR_BACKGROUND = (30, 30, 30)
COLOR_BANNER = (26, 82, 118)      # Azul para el banner
COLOR_TEXT = (255, 255, 255)       # Texto blanco
COLOR_ACCENT = (241, 196, 15)     # Amarillo/dorado para resaltados
COLOR_SNAKE = (46, 204, 113)
COLOR_APPLE = (231, 76, 60)
COLOR_GAME_OVER_TITLE = (231, 76, 60)

# Fuentes
FONT_BANNER = pygame.font.SysFont("Arial", 16, bold=True)
FONT_SCORE = pygame.font.SysFont("Arial", 15, bold=True)
FONT_GAME_OVER = pygame.font.SysFont("Arial", 42, bold=True)
FONT_RESTART = pygame.font.SysFont("Arial", 22, bold=True)

# Frases de presentación personal
PRESENTATION_PHRASES = [
    "¡Hola! Soy Adonay Navas.",
    "Estudio Técnico en Ingeniería en Computación.",
    "Me apasiona el desarrollo de software y la arquitectura backend.",
    "Actualmente trabajo en proyectos con Java en Spring Boot otros proyectos en larevel 12, en frontend con vue y react utilizando el gestor de base de datos PosgresSQL",
    "¡Has completado mi presentación! Sigue jugando para superar tu récord."
]

# Inicializar ventana
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Juego Snake - Presentación Adonay Navas")

# Reloj para controlar los FPS
clock = pygame.time.Clock()
FPS = 10

def draw_wrapped_text(surface, text, font, color, max_width, start_y):
    """Divide el texto en varias líneas si sobrepasa max_width y lo dibuja centrado."""
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))

    # Dibujar cada línea centrada horizontalmente
    line_height = font.get_linesize()
    total_height = len(lines) * line_height
    y = start_y - (total_height // 2)

    for line in lines:
        line_surface = font.render(line, True, color)
        line_rect = line_surface.get_rect(center=(WINDOW_WIDTH // 2, y))
        surface.blit(line_surface, line_rect)
        y += line_height

def generate_apple_position(snake_body):
    """Genera una posición aleatoria para la manzana en el área jugable (debajo del banner)."""
    while True:
        x = random.randrange(0, WINDOW_WIDTH, GRID_SIZE)
        y = random.randrange(BANNER_HEIGHT, WINDOW_HEIGHT, GRID_SIZE)
        if (x, y) not in snake_body:
            return (x, y)

def show_game_over_screen(screen, apples_eaten):
    """Muestra un panel semitransparente con la puntuación y opción de reinicio."""
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))

    screen.blit(overlay, (0, 0))

    title_surface = FONT_GAME_OVER.render("¡GAME OVER!", True, COLOR_GAME_OVER_TITLE)
    title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
    screen.blit(title_surface, title_rect)

    score_surface = FONT_BANNER.render(f"Puntuación Final: {apples_eaten} manzana(s)", True, COLOR_TEXT)
    score_rect = score_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(score_surface, score_rect)

    restart_surface = FONT_RESTART.render("Presiona 'R' para reiniciar o 'Q' para salir", True, COLOR_ACCENT)
    restart_rect = restart_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
    screen.blit(restart_surface, restart_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(15)

def run_game():
    start_x = WINDOW_WIDTH // 2
    start_y = BANNER_HEIGHT + (GAME_HEIGHT // 2)
    start_x = (start_x // GRID_SIZE) * GRID_SIZE
    start_y = (start_y // GRID_SIZE) * GRID_SIZE

    snake = [(start_x, start_y), (start_x - GRID_SIZE, start_y), (start_x - (2 * GRID_SIZE), start_y)]
    
    direction = (GRID_SIZE, 0)
    next_direction = direction

    apples_eaten = 0
    apple = generate_apple_position(snake)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, GRID_SIZE):
                    next_direction = (0, -GRID_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -GRID_SIZE):
                    next_direction = (0, GRID_SIZE)
                elif event.key == pygame.K_LEFT and direction != (GRID_SIZE, 0):
                    next_direction = (-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-GRID_SIZE, 0):
                    next_direction = (GRID_SIZE, 0)

        direction = next_direction

        head_x, head_y = snake[0]
        dir_x, dir_y = direction
        new_head = (head_x + dir_x, head_y + dir_y)

        if new_head[0] < 0 or new_head[0] >= WINDOW_WIDTH or new_head[1] < BANNER_HEIGHT or new_head[1] >= WINDOW_HEIGHT:
            running = False
            break

        if new_head in snake:
            running = False
            break

        snake.insert(0, new_head)

        if new_head == apple:
            apples_eaten += 1
            apple = generate_apple_position(snake)
        else:
            snake.pop()

        screen.fill(COLOR_BACKGROUND)

        # --- DIBUJAR BANNER SUPERIOR ---
        pygame.draw.rect(screen, COLOR_BANNER, (0, 0, WINDOW_WIDTH, BANNER_HEIGHT))
        pygame.draw.line(screen, COLOR_ACCENT, (0, BANNER_HEIGHT - 2), (WINDOW_WIDTH, BANNER_HEIGHT - 2), 2)

        phrase_index = min(apples_eaten, len(PRESENTATION_PHRASES) - 1)
        current_phrase = PRESENTATION_PHRASES[phrase_index]

        # Renderizar texto de la frase con Word-Wrap
        draw_wrapped_text(screen, current_phrase, FONT_BANNER, COLOR_TEXT, WINDOW_WIDTH - 40, 38)

        # Renderizar contador de manzanas
        score_surface = FONT_SCORE.render(f"Manzanas: {apples_eaten}", True, COLOR_ACCENT)
        score_rect = score_surface.get_rect(center=(WINDOW_WIDTH // 2, BANNER_HEIGHT - 18))
        screen.blit(score_surface, score_rect)

        # --- DIBUJAR ELEMENTOS DEL JUEGO ---
        pygame.draw.rect(screen, COLOR_APPLE, (apple[0], apple[1], GRID_SIZE, GRID_SIZE))

        for segment in snake:
            pygame.draw.rect(screen, COLOR_SNAKE, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

        pygame.display.flip()
        clock.tick(FPS)

    show_game_over_screen(screen, apples_eaten)

def main():
    while True:
        run_game()

if __name__ == "__main__":
    main()



