import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 600, 600
FPS = 60
BRICK_WIDTH, BRICK_HEIGHT = 98, 38
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_RADIUS = 10

# Colors
GREEN = (28, 252, 106)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (252, 3, 152)
ORANGE = (252, 170, 28)
RED = (255, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker Game")
clock = pygame.time.Clock()

# Paddle and ball
floor = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT - PADDLE_HEIGHT - BALL_RADIUS * 2 - 20, BALL_RADIUS * 2, BALL_RADIUS * 2)

# Ball movement
move = [random.choice([-1, 1]), -1]
ball_speed = 5

# Paddle movement
paddle_speed = 8
move_left = move_right = False

# Bricks
bricks = [pygame.Rect(1 + i * BRICK_WIDTH, 60 + j * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT) for i in range(6) for j in range(3)]

# Power-ups
power_ups = []

# Game variables
score = 0
lives = 3
level = 1
paused = False
continue_game = True
game_over = False  # Define the game_over variable

# Function to reset the game state
def reset_game():
    global score, level, paused, move, bricks, power_ups, lives, game_over
    score = 0
    level = 1
    paused = False
    game_over = False
    move = [random.choice([-1, 1]), -1]
    bricks = [pygame.Rect(1 + i * BRICK_WIDTH, 60 + j * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT) for i in range(6) for j in range(3)]
    power_ups = []
    lives = 3
    # Reset ball position on top of the paddle
    ball.x = WIDTH // 2 - BALL_RADIUS
    ball.y = HEIGHT - PADDLE_HEIGHT - BALL_RADIUS * 2 - 20

# Main game loop
while continue_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continue_game = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Press Enter to start the game and close the opening window
                continue_game = False
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_LEFT:
                move_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_LEFT:
                move_left = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if restart_button.collidepoint(mouse_x, mouse_y):
                reset_game()  # Reset the game state
            elif exit_button.collidepoint(mouse_x, mouse_y):
                continue_game = False

    if not paused and not game_over:
        # Update game elements
        ball.x += move[0] * ball_speed
        ball.y += move[1] * ball_speed

        # Paddle movement
        if move_right and floor.x < WIDTH - PADDLE_WIDTH:
            floor.x += paddle_speed
        if move_left and floor.x > 0:
            floor.x -= paddle_speed

        # Ball collisions
        if ball.x > WIDTH - BALL_RADIUS or ball.x < BALL_RADIUS:
            move[0] = -move[0]
        if ball.y < BALL_RADIUS:
            move[1] = -move[1]
        if floor.colliderect(ball):
            move[1] = -move[1]

        # Check if the ball hits the bottom
        if ball.y > HEIGHT - BALL_RADIUS:
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                ball.x = WIDTH // 2 - BALL_RADIUS
                ball.y = HEIGHT - PADDLE_HEIGHT - BALL_RADIUS * 2 - 20
                move = [random.choice([-1, 1]), -1]

        # Check for collisions with bricks
        for brick in bricks:
            if brick.colliderect(ball):
                bricks.remove(brick)
                move[1] = -move[1]
                score += 1

                # Add a power-up randomly
                if random.randint(1, 10) == 1:
                    power_ups.append(pygame.Rect(brick.centerx - 10, brick.centery - 10, 20, 20))

        # Check for power-up collection
        for power_up in power_ups:
            if power_up.colliderect(floor):
                power_ups.remove(power_up)
                # Implement power-up effects here (e.g., increase paddle size, extra life, etc.)

        # Check for level completion
        if not bricks:
            level += 1
            ball_speed += 1
            bricks = [pygame.Rect(1 + i * BRICK_WIDTH, 60 + j * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT) for i in range(6) for j in range(3)]

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, PINK, floor)
    pygame.draw.circle(screen, WHITE, ball.center, BALL_RADIUS)

    for brick in bricks:
        pygame.draw.rect(screen, ORANGE, brick)

    font = pygame.font.Font(None, 34)
    text = font.render(f"LEVEL: {level}  SCORE: {score}  LIVES: {lives}", 1, WHITE)
    screen.blit(text, (10, 10))

    if game_over:
        # Draw the game over screen
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER!", 1, RED)
        screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))

        # Draw the restart button
        restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)
        pygame.draw.rect(screen, GREEN, restart_button)
        font = pygame.font.Font(None, 34)
        text = font.render("RESTART", 1, BLACK)
        screen.blit(text, (WIDTH // 2 - 50, HEIGHT // 2 + 135))

        # Draw the exit button
        exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 200, 200, 50)
        pygame.draw.rect(screen, RED, exit_button)
        font = pygame.font.Font(None, 34)
        text = font.render("EXIT", 1, BLACK)
        screen.blit(text, (WIDTH // 2 - 35, HEIGHT // 2 + 215))

    pygame.display.flip()
    clock.tick(FPS)

# End the game
pygame.quit()
sys.exit()
