from player import *
from objects import *
def show_start_screen(screen):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Runner Game", True, BLACK)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))

    font = pygame.font.Font(None, 36)
    text = font.render("Press SPACE to start", True, BLACK)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 + 50))

    pygame.display.flip()

def show_end_screen(screen, score, state):
    screen.fill(WHITE)
    if state == 0:
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, BLACK)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
    else:
        font = pygame.font.Font(None, 74)
        text = font.render("Level complete!", True, BLACK)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 + 50))

    text = font.render("Press SPACE to restart", True, BLACK)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 + 150))

    pygame.display.flip()


background_img = pygame.image.load("city (1).jpg")
background_width = background_img.get_width()

camera_x = 0
def main():
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Runner Game")
    clock = pygame.time.Clock()

    game_state = "start"
    state = 0

    while True:
        if game_state == "start":
            show_start_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = "game"
                        player = Player()
                        enemies = [
                            Enemy(1000, screen_height - ENEMY_HEIGHT - 100),
                            Enemy(3000, screen_height - ENEMY_HEIGHT - 100),
                            Enemy(5000, screen_height - ENEMY_HEIGHT - 100),
                            Enemy(7000, screen_height - ENEMY_HEIGHT - 100),
                            Enemy(9000, screen_height - ENEMY_HEIGHT - 100),
                            Enemy(12000, screen_height - ENEMY_HEIGHT - 100),
                            Enemy(15000, screen_height - ENEMY_HEIGHT - 100),
                            Enemy(18000, screen_height - ENEMY_HEIGHT - 100),
                        ]
                        obstacles = [
                            Obstacle(600, screen_height - 150),
                            Obstacle(1100, screen_height - 150),
                            Obstacle(2000, screen_height - 150),
                            Obstacle(3000, screen_height - 150),
                            Obstacle(4000, screen_height - 150),
                            Obstacle(5000, screen_height - 150),
                            Obstacle(6000, screen_height - 150),
                            Obstacle(7000, screen_height - 150),
                            Obstacle(8000, screen_height - 150),
                            Obstacle(9000, screen_height - 150),
                        ]
                        platforms = [
                            Platform(1500, screen_height - 300, 200, 20),
                            Platform(2500, screen_height - 400, 200, 20),
                            Platform(3500, screen_height - 500, 200, 20),
                            Platform(4500, screen_height - 600, 200, 20),
                            Platform(5500, screen_height - 700, 200, 20),
                            Platform(6500, screen_height - 800, 200, 20),
                            Platform(7500, screen_height - 900, 200, 20),
                            Platform(8500, screen_height - 1000, 200, 20),
                        ]
                        coins = [
                            Coin(1600, screen_height - 350),
                            Coin(2600, screen_height - 450),
                            Coin(3600, screen_height - 550),
                            Coin(4600, screen_height - 650),
                            Coin(5600, screen_height - 750),
                            Coin(6600, screen_height - 850),
                            Coin(7600, screen_height - 950),
                            Coin(8600, screen_height - 1050),
                            Coin(9600, screen_height - 1150),
                            Coin(10600, screen_height - 1250),
                            Coin(11600, screen_height - 1350),
                            Coin(12600, screen_height - 1450),
                        ]
                        spikes = [
                            Spike(1800, screen_height - 120, 50, 50),
                            Spike(2800, screen_height - 120, 50, 50),
                            Spike(3800, screen_height - 120, 50, 50),
                            Spike(4800, screen_height - 120, 50, 50),
                            Spike(5800, screen_height - 120, 50, 50),
                            Spike(6800, screen_height - 120, 50, 50),
                            Spike(7800, screen_height - 120, 50, 50),
                            Spike(8800, screen_height - 120, 50, 50),
                            Spike(9800, screen_height - 120, 50, 50),
                            Spike(10800, screen_height - 120, 50, 50),
                            Spike(11800, screen_height - 120, 50, 50),
                            Spike(12800, screen_height - 120, 50, 50),
                        ]
                        camera_x = 0

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

            background_offset = camera_x % background_width
            screen.blit(background_img, (-background_offset, 0))
            screen.blit(background_img, (background_width - background_offset, 0))

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

            for spike in spikes:
                spike.draw(screen, camera_x)
                if player.rect.colliderect(spike.rect):
                    player.health -= 10
                    if player.health <= 0:
                        game_state = "end"

            for enemy in enemies[:]:
                enemy.update(player)
                enemy.draw(screen, camera_x)

                if enemy.health <= 0:
                    enemies.remove(enemy)

                if enemy.is_in_attack_range(player):
                    player.health -= 0.3
            if player.health <= 0:
                game_state = "end"

            player.draw(screen, camera_x)

            if player.rect.x >= level_width - player.rect.width:
                state = 1
                game_state = "end"

            pygame.display.flip()
            clock.tick(60)

        elif game_state == "end":
            show_end_screen(screen, player.score, state)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = "start"

if __name__ == "__main__":
    main()