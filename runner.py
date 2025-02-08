import sqlite3
from player import *
from objects import *

pygame.init()
pygame.mixer.init()


def load_level_1():
    return {
        "background": "city (1).jpg",
        "music": "1. Blast Off! FULL.mp3",
        "enemies": [
            Enemy(1000, screen_height - ENEMY_HEIGHT - 100),
            Enemy(2000, screen_height - ENEMY_HEIGHT - 100),
            Enemy(3000, screen_height - ENEMY_HEIGHT - 100),
            Enemy(4000, screen_height - ENEMY_HEIGHT - 100),
            Enemy(5000, screen_height - ENEMY_HEIGHT - 100),
        ],
        "obstacles": [
            Obstacle(600, screen_height - 150, "trashbin", width=70, height=70),
            Obstacle(1100, screen_height - 150, "wall", width=100, height=70),
            Obstacle(1600, screen_height - 150, "barrel", width=100, height=80),
            Obstacle(2100, screen_height - 150, "manhole", width=100, height=80),
            Obstacle(2600, screen_height - 150, "trashbin", width=70, height=70),
            Obstacle(3100, screen_height - 150, "wall", width=100, height=70),
            Obstacle(3600, screen_height - 150, "barrel", width=100, height=80),
            Obstacle(4100, screen_height - 150, "manhole", width=100, height=80),
            Obstacle(4600, screen_height - 150, "wall", width=100, height=70),
            Obstacle(5100, screen_height - 150, "barrel", width=100, height=80),
        ],
        "platforms": [
            Platform(1500, screen_height - 300, 200, 20),
            Platform(1800, screen_height - 400, 200, 20),
            Platform(3500, screen_height - 300, 200, 20),
            Platform(3800, screen_height - 400, 200, 20),
            Platform(4100, screen_height - 500, 200, 20),
        ],
        "coins": [
            Coin(1600, screen_height - 350),
            Coin(1800, screen_height - 350),
            Coin(2000, screen_height - 450),
            Coin(2200, screen_height - 450),
            Coin(2800, screen_height - 150),
            Coin(3000, screen_height - 150),
            Coin(3200, screen_height - 150),
            Coin(3600, screen_height - 350),
            Coin(3800, screen_height - 450),
            Coin(4000, screen_height - 550),
            Coin(4200, screen_height - 550),
            Coin(4600, screen_height - 150),
            Coin(4800, screen_height - 150),
        ],
    }


def load_level_2():
    return {
        "background": "41530[1].jpg",
        "music": "4. Inside the Robot Factory FULL.mp3",
        "enemies": [
            Enemy(2000, screen_height - ENEMY_HEIGHT - 100),
            Enemy(3000, screen_height - ENEMY_HEIGHT - 100),
            Enemy(4000, screen_height - ENEMY_HEIGHT - 100),
            Enemy(5000, screen_height - ENEMY_HEIGHT - 100),

        ],
        "obstacles": [
            Obstacle(800, screen_height - 150, "wall", width=100, height=70),
            Obstacle(1500, screen_height - 150, "log", width=110, height=80),
            Obstacle(2200, screen_height - 150, "log", width=110, height=80),
            Obstacle(2800, screen_height - 150, "log", width=110, height=80),
            Obstacle(3400, screen_height - 150, "wall", width=100, height=70),
            Obstacle(4000, screen_height - 150, "log", width=110, height=80),
            Obstacle(4600, screen_height - 150, "wall", width=100, height=70),
            Obstacle(5200, screen_height - 150, "wall", width=100, height=70),
        ],
        "platforms": [
            Platform(2100, screen_height - 300, 200, 20),
            Platform(2500, screen_height - 400, 200, 20),
            Platform(2800, screen_height - 500, 200, 20),
            Platform(4000, screen_height - 300, 200, 20),
            Platform(4300, screen_height - 400, 200, 20),
            Platform(4600, screen_height - 500, 200, 20),
        ],
        "coins": [
            Coin(2100, screen_height - 350),
            Coin(2300, screen_height - 350),
            Coin(2500, screen_height - 450),
            Coin(2700, screen_height - 450),
            Coin(2800, screen_height - 550),
            Coin(3000, screen_height - 550),
            Coin(4000, screen_height - 350),
            Coin(4200, screen_height - 350),
            Coin(4400, screen_height - 450),
            Coin(4600, screen_height - 550),
            Coin(4800, screen_height - 550),
        ],
    }


def create_db():
    conn = sqlite3.connect('player_progress.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            levels_completed INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def save_progress(levels_completed):
    conn = sqlite3.connect('player_progress.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO player_progress (levels_completed) VALUES (?)', (levels_completed,))
    conn.commit()
    conn.close()


def get_progress():
    conn = sqlite3.connect('player_progress.db')
    cursor = conn.cursor()
    cursor.execute('SELECT levels_completed FROM player_progress ORDER BY id DESC LIMIT 1')
    progress = cursor.fetchone()
    conn.close()
    return progress[0] if progress else 0


def show_start_screen(screen):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Run and Live", True, BLACK)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))

    font = pygame.font.Font(None, 36)
    text = font.render("Press SPACE to start", True, BLACK)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 + 50))

    progress = get_progress()
    text = font.render(f"Levels completed: {progress}", True, BLACK)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 + 100))

    button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 150, 200, 50)
    pygame.draw.rect(screen, (0, 128, 255), button_rect)
    button_text = font.render("Top Progress", True, WHITE)
    screen.blit(button_text, (button_rect.x + 20, button_rect.y + 10))

    pygame.display.flip()
    return button_rect


def show_top_progress(screen):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    text = font.render("Player Progress", True, BLACK)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 50))

    progress = get_progress()
    text = font.render(f"Levels completed: {progress}", True, BLACK)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 100))

    back_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height - 100, 200, 50)
    pygame.draw.rect(screen, (0, 128, 255), back_button_rect)
    back_text = font.render("Back", True, WHITE)
    screen.blit(back_text, (back_button_rect.x + 20, back_button_rect.y + 10))

    pygame.display.flip()
    return back_button_rect


def show_end_screen(screen, score, state, levels_completed):
    screen.fill(WHITE)
    if state == 0:
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, BLACK)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 + 50))

        text = font.render("Press SPACE to restart", True, BLACK)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 + 150))
    else:
        font = pygame.font.Font(None, 74)
        text = font.render("Level complete!", True, BLACK)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
        font = pygame.font.Font(None, 36)
        text = font.render(f"Levels completed: {levels_completed}", True, BLACK)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 + 50))

        text = font.render("Press SPACE to start next level", True, BLACK)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 + 150))

    pygame.display.flip()


def show_final_screen(screen):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Congratulations!", True, BLACK)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 100))

    font = pygame.font.Font(None, 36)
    text = font.render("You have completed all levels!", True, BLACK)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2))

    button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 100, 200, 50)
    pygame.draw.rect(screen, (0, 128, 255), button_rect)
    button_text = font.render("Quit", True, WHITE)
    screen.blit(button_text, (button_rect.x + 60, button_rect.y + 10))

    pygame.display.flip()
    return button_rect


def reset_level(level_data):
    for enemy in level_data["enemies"]:
        enemy.rect.x = enemy.start_x
        enemy.health = enemy.max_health

    for coin in level_data["coins"]:
        coin.collected = False


def main():
    pygame.init()
    create_db()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Runner Game")
    clock = pygame.time.Clock()

    levels = [load_level_1(), load_level_2()]
    current_level = 0
    level_complete = False
    levels_completed = get_progress()

    level_data = levels[current_level]
    background_img = pygame.image.load(level_data["background"])
    background_width = background_img.get_width()
    camera_x = 0
    game_state = "start"
    state = 0

    while True:
        if game_state == "start":
            button_rect = show_start_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = "game"
                        player = Player()
                        level_data = levels[current_level]
                        reset_level(level_data)
                        background_img = pygame.image.load(level_data["background"])
                        pygame.mixer.music.load(level_data["music"])
                        pygame.mixer.music.play(-1)
                        enemies = level_data["enemies"]
                        obstacles = level_data["obstacles"]
                        platforms = level_data["platforms"]
                        coins = level_data["coins"]
                        camera_x = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        game_state = "top_progress"

        elif game_state == "top_progress":
            back_button_rect = show_top_progress(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(event.pos):
                        game_state = "start"

        elif game_state == "game":
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                player.jump()
            if keys[pygame.K_LEFT]:
                player.move("left")
            if keys[pygame.K_RIGHT]:
                player.move("right")
            if keys[pygame.K_SPACE]:
                player.attack()

            player.update()
            player.check_collision_with_obstacles(obstacles)

            if player.rect.x > screen_width - 400 and player.rect.x < level_width - screen_width + 400:
                camera_x = player.rect.x - (screen_width - 400)
            else:
                camera_x = max(0, min(camera_x, level_width - screen_width))

            background_offset = camera_x % background_width
            for x in range(-background_offset, screen_width, background_width - 14):
                screen.blit(background_img, (x,  0))

            for platform in platforms:
                platform.draw(screen, camera_x)
                if player.rect.colliderect(platform.rect) and player.velocity_y > 0:
                    player.rect.y = platform.rect.y - player.rect.height
                    player.is_jumping = False
                    player.velocity_y = 0

            for obstacle in obstacles:
                obstacle.draw(screen, camera_x)

            for coin in coins:
                if not coin.collected and player.rect.colliderect(coin.rect):
                    coin.collected = True
                    player.score += 1
                coin.draw(screen, camera_x)

            for enemy in enemies[:]:
                enemy.update(player)
                enemy.draw(screen, camera_x)

                if enemy.health <= 0:
                    enemies.remove(enemy)

                if enemy.is_in_attack_range(player):
                    player.health -= 0.3

            if player.health <= 0:
                game_state = "end"
                pygame.mixer.music.stop()

            player.draw(screen, camera_x)

            if player.rect.x >= level_width - player.rect.width - 500:
                level_complete = True
                game_state = "end"
                state = 1
                pygame.mixer.music.stop()

            pygame.display.flip()
            clock.tick(60)

        elif game_state == "end":
            if state == 1:
                levels_completed += 1
                save_progress(levels_completed)
                state = 0
            show_end_screen(screen, player.score, state, levels_completed)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if level_complete:
                            current_level += 1
                            if current_level >= len(levels):
                                game_state = "final"
                            else:
                                game_state = "start"
                                player.score = 0
                                level_complete = False
                        else:
                            game_state = "start"

        elif game_state == "final":
            quit_button_rect = show_final_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        return


if __name__ == "__main__":
    main()