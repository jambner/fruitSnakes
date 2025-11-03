import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🍉 FruitSnakes")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

# Game constants
START_SPEED = 10
SPEED_BOOST = 16
SPEED_SLOW = 6
NORMAL_FRUIT = "normal"
GOLDEN_FRUIT = "golden"
ROTTEN_FRUIT = "rotten"

# Helper functions
def random_cell():
    return (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))

def draw_cell(position, color):
    rect = pygame.Rect(position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)

def random_fruit_type():
    roll = random.random()
    if roll < 0.7:
        return NORMAL_FRUIT
    elif roll < 0.9:
        return GOLDEN_FRUIT
    else:
        return ROTTEN_FRUIT

def draw_text(text, x, y, color=WHITE):
    screen.blit(font.render(text, True, color), (x, y))

# Game loop
def main():
    snake = [(COLS // 2, ROWS // 2)]
    direction = (1, 0)
    next_dir = direction
    fruit_pos = random_cell()
    fruit_type = random_fruit_type()
    score = 0
    speed = START_SPEED
    boost_timer = 0

    running = True
    while running:
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    next_dir = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    next_dir = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    next_dir = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_dir = (1, 0)

        direction = next_dir
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Game over conditions
        if (
            new_head in snake or
            not (0 <= new_head[0] < COLS) or
            not (0 <= new_head[1] < ROWS)
        ):
            break

        snake.insert(0, new_head)

        # Fruit collision
        if new_head == fruit_pos:
            if fruit_type == NORMAL_FRUIT:
                score += 1
            elif fruit_type == GOLDEN_FRUIT:
                score += 5
                speed = SPEED_BOOST
                boost_timer = 50
                snake.extend([snake[-1]] * 2)
            elif fruit_type == ROTTEN_FRUIT:
                score -= 3
                speed = SPEED_SLOW
                boost_timer = 50
                if len(snake) > 3:
                    snake.pop()
                    snake.pop()
            fruit_pos = random_cell()
            fruit_type = random_fruit_type()
        else:
            snake.pop()

        # Speed timer decay
        if boost_timer > 0:
            boost_timer -= 1
            if boost_timer == 0:
                speed = START_SPEED

        # Draw frame
        screen.fill(BLACK)
        for segment in snake:
            draw_cell(segment, GREEN)

        # Draw fruit
        if fruit_type == NORMAL_FRUIT:
            draw_cell(fruit_pos, RED)
        elif fruit_type == GOLDEN_FRUIT:
            draw_cell(fruit_pos, YELLOW)
        elif fruit_type == ROTTEN_FRUIT:
            draw_cell(fruit_pos, BROWN)

        # Draw score
        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Speed: {speed}", 10, 35)

        pygame.display.flip()

    # Game over screen
    screen.fill(BLACK)
    draw_text("Game Over!", WIDTH // 2 - 70, HEIGHT // 2 - 20, RED)
    draw_text(f"Final Score: {score}", WIDTH // 2 - 80, HEIGHT // 2 + 20, WHITE)
    pygame.display.flip()
    pygame.time.wait(3000)

if __name__ == "__main__":
    main()
