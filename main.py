import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
HEADER_HEIGHT = 40  # Top banner

ROWS = (HEIGHT - HEADER_HEIGHT) // CELL_SIZE
COLS = WIDTH // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
HEADER_BG = (30, 30, 30)
GRAY = (100, 100, 100)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🍉 FruitSnakes")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)
toggle_font = pygame.font.SysFont("arial", 16)

# Game constants
START_SPEED = 6
SPEED_BOOST = 12
SPEED_SLOW = 4
NORMAL_FRUIT = "normal"
GOLDEN_FRUIT = "golden"
ROTTEN_FRUIT = "rotten"
MAX_BACKPACK = 3  # slots

# ---------- Helper Functions ----------
def random_cell():
    return (
        random.randint(0, COLS - 1),
        random.randint(HEADER_HEIGHT // CELL_SIZE, ROWS - 1)
    )

def spawn_fruit(snake):
    while True:
        pos = random_cell()
        if pos not in snake:
            return pos

def draw_cell(position, color):
    rect = pygame.Rect(
        position[0] * CELL_SIZE,
        position[1] * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )
    pygame.draw.rect(screen, color, rect)

def draw_text(text, x, y, color=WHITE, font_obj=None):
    f = font_obj if font_obj else font
    screen.blit(f.render(text, True, color), (x, y))

def restart_button():
    button_rect = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 + 60, 160, 40)
    pygame.draw.rect(screen, WHITE, button_rect)
    draw_text("Restart (R)", WIDTH // 2 - 60, HEIGHT // 2 + 70, BLACK)
    return button_rect

def random_fruit_type(first_fruit=False):
    if first_fruit:
        return NORMAL_FRUIT
    roll = random.random()
    if roll < 0.7:
        return NORMAL_FRUIT
    elif roll < 0.9:
        return GOLDEN_FRUIT
    else:
        return ROTTEN_FRUIT

# ---------- Game Loop ----------
def main():

    def reset_game():
        snake_start = [(COLS // 2, HEADER_HEIGHT // CELL_SIZE + 5)]
        first_fruit_type = random_fruit_type(first_fruit=True)
        return {
            "snake": snake_start,
            "direction": (1, 0),
            "next_dir": (1, 0),
            "fruit_pos": spawn_fruit(snake_start),
            "fruit_type": first_fruit_type,
            "extra_fruits": [],
            "score": 0,
            "speed": START_SPEED,
            "boost_timer": 0,
            "backpack_enabled": True,
            "backpack": []
        }

    game = reset_game()
    game_over = False
    running = True

    while running:
        clock.tick(game["speed"])

        # ---------- Event Handling ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Snake movement
                if not game_over:
                    if event.key == pygame.K_UP and game["direction"] != (0, 1):
                        game["next_dir"] = (0, -1)
                    elif event.key == pygame.K_DOWN and game["direction"] != (0, -1):
                        game["next_dir"] = (0, 1)
                    elif event.key == pygame.K_LEFT and game["direction"] != (1, 0):
                        game["next_dir"] = (-1, 0)
                    elif event.key == pygame.K_RIGHT and game["direction"] != (-1, 0):
                        game["next_dir"] = (1, 0)

                # Throw a fruit from backpack
                if event.key == pygame.K_SPACE and game["backpack"]:
                    if game["fruit_type"] == ROTTEN_FRUIT:
                        game["fruit_type"] = random.choice([NORMAL_FRUIT, GOLDEN_FRUIT])
                        game["fruit_pos"] = spawn_fruit(game["snake"])
                        game["backpack"].pop(0)

                # Toggle backpack on/off
                if event.key == pygame.K_y:
                    game["backpack_enabled"] = not game["backpack_enabled"]

                # Restart
                if game_over and event.key == pygame.K_r:
                    game = reset_game()
                    game_over = False

            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button().collidepoint(event.pos):
                    game = reset_game()
                    game_over = False

        if not game_over:
            # ---------- Move Snake ----------
            game["direction"] = game["next_dir"]
            new_head = (
                game["snake"][0][0] + game["direction"][0],
                game["snake"][0][1] + game["direction"][1]
            )

            # Collision with snake/body or walls
            if (
                new_head in game["snake"]
                or not (0 <= new_head[0] < COLS)
                or not (HEADER_HEIGHT // CELL_SIZE <= new_head[1] < ROWS)
            ):
                game_over = True

            game["snake"].insert(0, new_head)

            # ---------- Fruit Collision ----------
            if new_head == game["fruit_pos"]:
                # Normal fruit
                if game["fruit_type"] == NORMAL_FRUIT:
                    game["score"] += 1
                    if game["backpack_enabled"] and len(game["backpack"]) < MAX_BACKPACK:
                        game["backpack"].append(NORMAL_FRUIT)

                # Golden fruit
                elif game["fruit_type"] == GOLDEN_FRUIT:
                    if game["backpack_enabled"] and len(game["backpack"]) < MAX_BACKPACK:
                        # Collect into backpack, no speed boost
                        game["backpack"].append(GOLDEN_FRUIT)
                    else:
                        # Backpack OFF: eat directly, apply speed boost
                        game["score"] += 5
                        game["speed"] = SPEED_BOOST
                        game["boost_timer"] = 50

                # Rotten fruit
                elif game["fruit_type"] == ROTTEN_FRUIT:
                    if game["backpack_enabled"] and len(game["backpack"]) < MAX_BACKPACK:
                        # Collect rotten fruit into backpack
                        game["backpack"].append(ROTTEN_FRUIT)
                    else:
                        # Penalty if backpack OFF
                        game["score"] -= 3
                        game["speed"] = SPEED_SLOW
                        game["boost_timer"] = 50
                        if len(game["snake"]) > 3:
                            game["snake"].pop()
                            game["snake"].pop()

                # Spawn next fruit safely
                game["fruit_pos"] = spawn_fruit(game["snake"])
                game["fruit_type"] = random_fruit_type()

            else:
                game["snake"].pop()

            # ---------- Extra Fruits Collision ----------
            for extra in game["extra_fruits"][:]:
                if new_head == extra["pos"]:
                    game["score"] += 1 if extra["type"] == NORMAL_FRUIT else 5
                    if game["backpack_enabled"] and len(game["backpack"]) < MAX_BACKPACK:
                        game["backpack"].append(extra["type"])
                    game["extra_fruits"].remove(extra)

            # ---------- Speed Timer Decay ----------
            if game["boost_timer"] > 0:
                game["boost_timer"] -= 1
                if game["boost_timer"] == 0:
                    game["speed"] = START_SPEED

        # ---------- Drawing ----------
        screen.fill(BLACK)

        # HUD Banner
        pygame.draw.rect(screen, HEADER_BG, (0, 0, WIDTH, HEADER_HEIGHT))
        draw_text(f"Score: {game['score']}", 10, 10)
        draw_text(f"Speed: {game['speed']}", 200, 10)

        # Draw backpack slots (always show colors)
        for i in range(MAX_BACKPACK):
            x = WIDTH - 30 * (MAX_BACKPACK - i)
            y = 5
            color = GRAY
            if i < len(game["backpack"]):
                if game["backpack"][i] == NORMAL_FRUIT:
                    color = RED
                elif game["backpack"][i] == GOLDEN_FRUIT:
                    color = YELLOW
                elif game["backpack"][i] == ROTTEN_FRUIT:
                    color = BROWN
            pygame.draw.rect(screen, color, (x, y, 20, 30))

        # Draw toggle text right next to first slot
        toggle_text = "Backpack: ON (Y)" if game["backpack_enabled"] else "Backpack: OFF (Y)"
        first_slot_x = WIDTH - 30 * MAX_BACKPACK
        text_x = first_slot_x - 140
        draw_text(toggle_text, text_x, 12, font_obj=toggle_font)

        if not game_over:
            # Draw snake
            for segment in game["snake"]:
                draw_cell(segment, GREEN)

            # Draw main fruit
            if game["fruit_type"] == NORMAL_FRUIT:
                draw_cell(game["fruit_pos"], RED)
            elif game["fruit_type"] == GOLDEN_FRUIT:
                draw_cell(game["fruit_pos"], YELLOW)
            elif game["fruit_type"] == ROTTEN_FRUIT:
                draw_cell(game["fruit_pos"], BROWN)

            # Draw extra fruits
            for extra in game["extra_fruits"]:
                draw_cell(extra["pos"], RED if extra["type"] == NORMAL_FRUIT else YELLOW if extra["type"] == GOLDEN_FRUIT else BROWN)

        else:
            draw_text("Game Over!", WIDTH // 2 - 70, HEIGHT // 2 - 30, RED)
            draw_text(f"Final Score: {game['score']}", WIDTH // 2 - 80, HEIGHT // 2 + 5)
            restart_button()

        pygame.display.flip()


# ---------- Start Game ----------
if __name__ == "__main__":
    main()
