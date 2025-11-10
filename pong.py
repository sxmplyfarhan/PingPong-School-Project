import pygame
import sys
import random
import time

# --- Initialize pygame ---
pygame.init()

# --- Virtual resolution ---
VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 800, 600

# --- Game settings ---

BALL_SPEED = 5
current_speed = BALL_SPEED
PADDLE_SPEED = 8
WIN_SCORE = 10
COLOR_SELECTION_TIME = 10  # seconds

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIN_COLOR = (0, 255, 0)
LOSE_COLOR = (255, 0, 0)

RAINBOW = [
    (255, 0, 0),       # Rosso
    (255, 127, 0),     # Arancione
    (255, 255, 0),     # Giallo
    (0, 255, 0),       # Verde
    (0, 0, 255),       # Blu
    (75, 0, 130),      # Indaco
    (148, 0, 211)      # Viola
]

# --- Fonts ---
FONT = pygame.font.Font(None, 50)
SCORE_FONT = pygame.font.Font(None, 36)

# --- Screen setup ---
screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Pong Due Giocatori")

# --- Virtual surface ---
virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

# --- Sound setup ---
pygame.mixer.init()
try:
    hit_sound = pygame.mixer.Sound("pong_hit.wav")
except:
    hit_sound = None

# --- Game objects ---
ball = pygame.Rect(VIRTUAL_WIDTH // 2 - 15, VIRTUAL_HEIGHT // 2 - 15, 30, 30)
paddle_left = pygame.Rect(20, VIRTUAL_HEIGHT // 2 - 70, 10, 140)
paddle_right = pygame.Rect(VIRTUAL_WIDTH - 30, VIRTUAL_HEIGHT // 2 - 70, 10, 140)

ball_speed_x = BALL_SPEED * random.choice((1, -1))
ball_speed_y = BALL_SPEED * random.choice((1, -1))

score_left = 0
score_right = 0

paddle_left_color = RAINBOW[0]
paddle_right_color = RAINBOW[1]


def color_menu_auto(player_name="Giocatore 1"):
    selected_index = 0
    start_time = time.time()
    while True:
        virtual_surface.fill(BLACK)
        # Title
        menu_title = FONT.render(f"Scegli colore {player_name}", True, WHITE)
        virtual_surface.blit(menu_title, (VIRTUAL_WIDTH // 2 - menu_title.get_width() // 2, VIRTUAL_HEIGHT * 0.08))

        # Color squares
        square_size = VIRTUAL_HEIGHT * 0.12
        spacing = (VIRTUAL_WIDTH - square_size * len(RAINBOW)) / (len(RAINBOW) + 1)
        for i, color in enumerate(RAINBOW):
            rect_x = spacing + i * (square_size + spacing)
            rect_y = VIRTUAL_HEIGHT * 0.4
            rect = pygame.Rect(rect_x, rect_y, square_size, square_size)
            pygame.draw.rect(virtual_surface, color, rect)
            if i == selected_index:
                pygame.draw.rect(virtual_surface, WHITE, rect, 4)

        remaining = max(0, COLOR_SELECTION_TIME - int(time.time() - start_time))
        info = SCORE_FONT.render(f"{remaining}s rimanenti", True, WHITE)
        virtual_surface.blit(info, (VIRTUAL_WIDTH // 2 - info.get_width() // 2, VIRTUAL_HEIGHT * 0.75))

        # Scale virtual surface to real screen
        screen.blit(pygame.transform.scale(virtual_surface, screen.get_size()), (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if player_name == "Giocatore 1":
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(RAINBOW)
                    if event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(RAINBOW)
                else:
                    if event.key == pygame.K_LEFT:
                        selected_index = (selected_index - 1) % len(RAINBOW)
                    if event.key == pygame.K_RIGHT:
                        selected_index = (selected_index + 1) % len(RAINBOW)

        if time.time() - start_time >= COLOR_SELECTION_TIME:
            return RAINBOW[selected_index]


def reset_ball():
    global ball_speed_x, ball_speed_y, current_speed
    ball.center = (VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 2)
    current_speed = 3  # slow restart
    ball_speed_x = current_speed * random.choice((1, -1))
    ball_speed_y = current_speed * random.choice((1, -1))



def move_ball():
    global ball_speed_x, ball_speed_y, score_left, score_right, current_speed

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= VIRTUAL_HEIGHT:
        if hit_sound:
            hit_sound.play()
        ball_speed_y *= -1

    if ball.left <= 0:
        score_right += 1
        reset_ball()
    if ball.right >= VIRTUAL_WIDTH:
        score_left += 1
        reset_ball()

    if ball.colliderect(paddle_left):
        if hit_sound:
            hit_sound.play()
        current_speed = min(current_speed + 0.4, BALL_SPEED * 1.8)
        ball_speed_x = abs(current_speed)
        ball_speed_y = random.choice([-current_speed, current_speed])
        ball.left = paddle_left.right + 1

    if ball.colliderect(paddle_right):
        if hit_sound:
            hit_sound.play()
        current_speed = min(current_speed + 0.4, BALL_SPEED * 1.8)
        ball_speed_x = -abs(current_speed)
        ball_speed_y = random.choice([-current_speed, current_speed])
        ball.right = paddle_right.left - 1




def pause_game():
    paused = True
    pause_text = FONT.render("PAUSA", True, WHITE)
    while paused:
        virtual_surface.fill(BLACK)
        virtual_surface.blit(pause_text, (VIRTUAL_WIDTH // 2 - pause_text.get_width() // 2, VIRTUAL_HEIGHT // 2 - 50))
        screen.blit(pygame.transform.scale(virtual_surface, screen.get_size()), (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
        pygame.time.wait(100)


def main():
    global paddle_left_color, paddle_right_color, score_left, score_right
    global screen

    clock = pygame.time.Clock()

    # Initial paddle colors
    paddle_left_color = color_menu_auto("Giocatore 1")
    paddle_right_color = color_menu_auto("Giocatore 2")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_game()
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        keys = pygame.key.get_pressed()

        # Paddle Left (↑ / ↓) — Giocatore 1
        if keys[pygame.K_UP] and paddle_left.top > 0:
            paddle_left.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and paddle_left.bottom < VIRTUAL_HEIGHT:
            paddle_left.y += PADDLE_SPEED

        # Paddle Right (← / →) — Giocatore 2
        if keys[pygame.K_LEFT] and paddle_right.top > 0:
            paddle_right.y -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and paddle_right.bottom < VIRTUAL_HEIGHT:
            paddle_right.y += PADDLE_SPEED


        move_ball()

        # --- Check for winner ---
        if score_left >= WIN_SCORE:
            virtual_surface.fill(BLACK)
            win_text = FONT.render("Giocatore 1 VINCE!", True, WIN_COLOR)
            virtual_surface.blit(win_text, (VIRTUAL_WIDTH // 2 - win_text.get_width() // 2, VIRTUAL_HEIGHT // 2 - 50))
            screen.blit(pygame.transform.scale(virtual_surface, screen.get_size()), (0, 0))
            pygame.display.flip()
            pygame.time.wait(2000)
            score_left = 0
            score_right = 0
            reset_ball()
            paddle_left_color = color_menu_auto("Giocatore 1")
            paddle_right_color = color_menu_auto("Giocatore 2")
        elif score_right >= WIN_SCORE:
            virtual_surface.fill(BLACK)
            win_text = FONT.render("Giocatore 2 VINCE!", True, WIN_COLOR)
            virtual_surface.blit(win_text, (VIRTUAL_WIDTH // 2 - win_text.get_width() // 2, VIRTUAL_HEIGHT // 2 - 50))
            screen.blit(pygame.transform.scale(virtual_surface, screen.get_size()), (0, 0))
            pygame.display.flip()
            pygame.time.wait(2000)
            score_left = 0
            score_right = 0
            reset_ball()
            paddle_left_color = color_menu_auto("Giocatore 1")
            paddle_right_color = color_menu_auto("Giocatore 2")

        # --- Draw ---
        virtual_surface.fill(BLACK)
        pygame.draw.rect(virtual_surface, paddle_left_color, paddle_left)
        pygame.draw.rect(virtual_surface, paddle_right_color, paddle_right)
        pygame.draw.ellipse(virtual_surface, WHITE, ball)
        pygame.draw.aaline(virtual_surface, WHITE, (VIRTUAL_WIDTH // 2, 0), (VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT))

        # Corner labels
        left_label = SCORE_FONT.render("Giocatore 1", True, WHITE)
        right_label = SCORE_FONT.render("Giocatore 2", True, WHITE)
        virtual_surface.blit(left_label, (VIRTUAL_WIDTH * 0.02, VIRTUAL_HEIGHT * 0.02))
        virtual_surface.blit(right_label, (VIRTUAL_WIDTH - right_label.get_width() - VIRTUAL_WIDTH * 0.02, VIRTUAL_HEIGHT * 0.02))

        # Center score
        if score_left > score_right:
            left_color, right_color = WIN_COLOR, LOSE_COLOR
            left_size, right_size = int(VIRTUAL_HEIGHT * 0.12), int(VIRTUAL_HEIGHT * 0.08)
        elif score_right > score_left:
            left_color, right_color = LOSE_COLOR, WIN_COLOR
            left_size, right_size = int(VIRTUAL_HEIGHT * 0.08), int(VIRTUAL_HEIGHT * 0.12)
        else:
            left_color = right_color = WHITE
            left_size = right_size = int(VIRTUAL_HEIGHT * 0.1)

        left_font = pygame.font.Font(None, left_size)
        right_font = pygame.font.Font(None, right_size)
        left_score = left_font.render(f"{score_left}", True, left_color)
        right_score = right_font.render(f"{score_right}", True, right_color)

        virtual_surface.blit(left_score, (VIRTUAL_WIDTH // 2 - 50 - left_score.get_width() // 2, 10))
        virtual_surface.blit(right_score, (VIRTUAL_WIDTH // 2 + 50 - right_score.get_width() // 2, 10))

        # --- Scale and display ---
        screen.blit(pygame.transform.scale(virtual_surface, screen.get_size()), (0, 0))
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
