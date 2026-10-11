import pygame
import random
import sys
from agent import PresentationAgent

# Inicializar Pygame
pygame.init()
pygame.font.init()

# Configuración de la pantalla y el área de juego
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700  # 600px de área jugable + 100px de banner superior
BANNER_HEIGHT = 100
GAME_HEIGHT = WINDOW_HEIGHT - BANNER_HEIGHT
GRID_SIZE = 20

# Colores (RGB)
COLOR_BACKGROUND = (30, 30, 30)
COLOR_BANNER = (26, 82, 118)
COLOR_TEXT = (255, 255, 255)
COLOR_ACCENT = (241, 196, 15)
COLOR_SNAKE = (46, 204, 113)
COLOR_APPLE = (231, 76, 60)
COLOR_GAME_OVER_TITLE = (231, 76, 60)

# Fuentes
FONT_BANNER = pygame.font.SysFont("Arial", 16, bold=True)
FONT_SCORE = pygame.font.SysFont("Arial", 15, bold=True)
FONT_GAME_OVER = pygame.font.SysFont("Arial", 36, bold=True)
FONT_FEEDBACK = pygame.font.SysFont("Arial", 16, bold=False)
FONT_RESTART = pygame.font.SysFont("Arial", 20, bold=True)

# Instancia del Agente
agent = PresentationAgent()

# Inicializar ventana y reloj
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Juego Snake - Sistema Agéntico Adonay Navas")
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

    line_height = font.get_linesize()
    total_height = len(lines) * line_height
    y = start_y - (total_height // 2)

    for line in lines:
        line_surface = font.render(line, True, color)
        line_rect = line_surface.get_rect(center=(WINDOW_WIDTH // 2, y))
        surface.blit(line_surface, line_rect)
        y += line_height

def generate_apple_position(snake_body):
    """Genera una posición aleatoria para la manzana en el área jugable."""
    while True:
        x = random.randrange(0, WINDOW_WIDTH, GRID_SIZE)
        y = random.randrange(BANNER_HEIGHT, WINDOW_HEIGHT, GRID_SIZE)
        if (x, y) not in snake_body:
            return (x, y)

def show_game_over_screen(screen, apples_eaten):
    """Muestra el panel de fin de juego invocando la retroalimentación del agente."""
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # Título
    title_surface = FONT_GAME_OVER.render("¡GAME OVER!", True, COLOR_GAME_OVER_TITLE)
    title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
    screen.blit(title_surface, title_rect)

    # Puntuación
    score_surface = FONT_BANNER.render(f"Puntuación Final: {apples_eaten} manzana(s)", True, COLOR_TEXT)
    score_rect = score_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
    screen.blit(score_surface, score_rect)

    # Retroalimentación generada por la Skill a través del Agente
    feedback_text = agent.evaluate_performance(apples_eaten)
    draw_wrapped_text(screen, feedback_text, FONT_FEEDBACK, COLOR_ACCENT, WINDOW_WIDTH - 60, WINDOW_HEIGHT // 2 + 20)

    # Instrucción de reinicio
    restart_surface = FONT_RESTART.render("Presiona 'R' para reiniciar o 'Q' para salir", True, COLOR_TEXT)
    restart_rect = restart_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
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
    start_x = (WINDOW_WIDTH // 2 // GRID_SIZE) * GRID_SIZE
    start_y = ((BANNER_HEIGHT + (GAME_HEIGHT // 2)) // GRID_SIZE) * GRID_SIZE

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

        # Dibujar Banner Superior
        pygame.draw.rect(screen, COLOR_BANNER, (0, 0, WINDOW_WIDTH, BANNER_HEIGHT))
        pygame.draw.line(screen, COLOR_ACCENT, (0, BANNER_HEIGHT - 2), (WINDOW_WIDTH, BANNER_HEIGHT - 2), 2)

        # Obtener frase dinámica mediante la Skill invocada por el Agente
        current_phrase = agent.get_current_phrase(apples_eaten)
        draw_wrapped_text(screen, current_phrase, FONT_BANNER, COLOR_TEXT, WINDOW_WIDTH - 40, 38)

        # Contador de manzanas
        score_surface = FONT_SCORE.render(f"Manzanas: {apples_eaten}", True, COLOR_ACCENT)
        score_rect = score_surface.get_rect(center=(WINDOW_WIDTH // 2, BANNER_HEIGHT - 18))
        screen.blit(score_surface, score_rect)

        # Dibujar Manzana y Snake
        pygame.draw.rect(screen, COLOR_APPLE, (apple[0], apple[1], GRID_SIZE, GRID_SIZE))
        for segment in snake:
            pygame.draw.rect(screen, COLOR_SNAKE, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

        pygame.display.flip()
        clock.tick(FPS)

    show_game_over_screen(screen, apples_eaten)
