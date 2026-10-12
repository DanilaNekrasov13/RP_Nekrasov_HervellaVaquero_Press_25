import pygame
import random
import sys

pygame.init()

# --- SETTINGS (Screen size) ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Python Game")

# --- COLORS ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)  # Player must be purple!
RED = (255, 0, 0)

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

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def reset_game():
    global player_x, player_y, enemy_x, enemy_y, score, enemy_speed
    player_x = WIDTH // 2
    player_y = HEIGHT - player_size - 10
    enemy_x = random.randint(0, WIDTH - enemy_size)
    enemy_y = -enemy_size
    score = 0
    enemy_speed = 5

# --- MAIN LOOP ---
def main():
    global player_x, enemy_x, enemy_y, score, enemy_speed
    
    clock = pygame.time.Clock()
    running = True
    game_over = False
    show_welcome = True

    while running:
        # 1. WELCOME SCREEN
        if show_welcome:
            screen.fill(BLACK)
            draw_text("Press any key to start", font, WHITE, 250, HEIGHT // 2)
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
                    print("Game restarted!")  # debug message

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
        screen.fill(BLACK)
        
        if not game_over:
            pygame.draw.rect(screen, PURPLE, (player_x, player_y, player_size, player_size))
            pygame.draw.rect(screen, RED, (enemy_x, enemy_y, enemy_size, enemy_size))
            draw_text(f"Score: {score}", font, WHITE, 10, 10)
        else:
            draw_text("GAME OVER!", font, RED, WIDTH // 2 - 80, HEIGHT // 2 - 50)
            draw_text(f"Your score: {score}", font, WHITE, WIDTH // 2 - 80, HEIGHT // 2)
            draw_text("Press R to play again", font, WHITE, WIDTH // 2 - 130, HEIGHT // 2 + 50)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()