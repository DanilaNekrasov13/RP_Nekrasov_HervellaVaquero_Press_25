import pygame
import random
import sys

pygame.init()

# --- SETTINGS (Screen size) ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Falling Blocks")

# --- COLORS ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (20, 20, 50)
LIGHT_BLUE = (40, 40, 90)
PURPLE = (160, 80, 220)
PURPLE_DARK = (100, 40, 160)
RED = (220, 60, 60)
YELLOW = (255, 220, 100)
CYAN = (100, 220, 220)

# --- PLAYER ---
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT - player_size - 10
player_speed = 5

# --- ENEMIES ---
enemy_size = 50
enemy_x = random.randint(0, WIDTH - enemy_size)
enemy_y = -enemy_size
enemy_speed = 5

# --- SCORE ---
score = 0
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# --- BACKGROUND STARS ---
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)) for _ in range(60)]


def draw_text(text, font, color, x, y, shadow=True):
    if shadow:
        shadow_img = font.render(text, True, (0, 0, 0))
        screen.blit(shadow_img, (x + 2, y + 2))
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_background():
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(DARK_BLUE[0] * (1 - ratio) + LIGHT_BLUE[0] * ratio)
        g = int(DARK_BLUE[1] * (1 - ratio) + LIGHT_BLUE[1] * ratio)
        b = int(DARK_BLUE[2] * (1 - ratio) + LIGHT_BLUE[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    for (sx, sy, size) in stars:
        pygame.draw.circle(screen, (200, 200, 230), (sx, sy), size)


def draw_player(x, y, size):
    center = (x + size // 2, y + size // 2)
    radius = size // 2
    pygame.draw.circle(screen, (60, 20, 100), center, radius + 4)
    pygame.draw.circle(screen, PURPLE, center, radius)
    pygame.draw.circle(screen, PURPLE_DARK, center, radius, 3)
    pygame.draw.circle(screen, WHITE, (center[0] - 8, center[1] - 5), 4)
    pygame.draw.circle(screen, WHITE, (center[0] + 8, center[1] - 5), 4)
    pygame.draw.circle(screen, BLACK, (center[0] - 8, center[1] - 5), 2)
    pygame.draw.circle(screen, BLACK, (center[0] + 8, center[1] - 5), 2)


def draw_enemy(x, y, size):
    cx = x + size // 2
    cy = y + size // 2
    half = size // 2
    points = [
        (cx, cy - half),
        (cx + half, cy),
        (cx, cy + half),
        (cx - half, cy)
    ]
    pygame.draw.polygon(screen, (100, 20, 20), [(p[0], p[1] + 4) for p in points])
    pygame.draw.polygon(screen, RED, points)
    pygame.draw.polygon(screen, (255, 120, 120), points, 3)
    pygame.draw.circle(screen, YELLOW, (cx, cy), 4)


def reset_game():
    global player_x, player_y, enemy_x, enemy_y, score, enemy_speed
    player_x = WIDTH // 2
    player_y = HEIGHT - player_size - 10
    enemy_x = random.randint(0, WIDTH - enemy_size)
    enemy_y = -enemy_size
    score = 0
    enemy_speed = 5


def main():
    global player_x, enemy_x, enemy_y, score, enemy_speed

    clock = pygame.time.Clock()
    running = True
    game_over = False
    show_welcome = True

    while running:
        # 1. WELCOME SCREEN
        if show_welcome:
            draw_background()
            title = big_font.render("DODGE THE BLOCKS", True, PURPLE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))
            draw_text("Press any key to start", font, WHITE, WIDTH // 2 - 130, HEIGHT // 2 + 20)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    show_welcome = False
            continue

        # 2. EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    reset_game()
                    game_over = False

        if not game_over:
            # 3. PLAYER CONTROLS
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
                player_x += player_speed

            # 4. ENEMY MOVEMENT
            enemy_y += enemy_speed
            if enemy_y > HEIGHT:
                enemy_y = -enemy_size
                enemy_x = random.randint(0, WIDTH - enemy_size)
                score += 1
                enemy_speed += 0.5

            # 5. COLLISION DETECTION
            player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
            enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)
            if player_rect.colliderect(enemy_rect):
                game_over = True

        # 6. DRAWING
        draw_background()

        if not game_over:
            draw_enemy(enemy_x, enemy_y, enemy_size)
            draw_player(player_x, player_y, player_size)
            draw_text(f"Score: {score}", font, CYAN, 15, 15)
        else:
            draw_text("GAME OVER", big_font, RED, WIDTH // 2 - 180, HEIGHT // 2 - 100)
            draw_text(f"Your score: {score}", font, WHITE, WIDTH // 2 - 80, HEIGHT // 2 - 10)
            draw_text("Press R to play again", font, CYAN, WIDTH // 2 - 130, HEIGHT // 2 + 50)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()