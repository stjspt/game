import pygame
import sys
import os

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 128, 255)
ENEMY_COLOR = (0, 255, 0)
FALL_COLOR = (0, 0, 255)
ATTACK_COLOR = (255, 165, 0)

GRAVITY = 1
JUMP_STRENGTH = 15
ENEMY_WIDTH = 140
ENEMY_HEIGHT = 140
FALL_WIDTH = 50
FALL_HEIGHT = 50

screen_width = 1500
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Runner Game")
clock = pygame.time.Clock()

level_width = 10000


def load_image(name, colorkey=None):
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Player:
    def __init__(self):
        self.image = load_image("idle.png")
        self.image = self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 140))
        self.rect = pygame.Rect(50, 240, 480, 500)
        self.velocity_y = 0
        self.is_jumping = False
        self.move_speed = 5
        self.health = 100
        self.is_attacking = False
        self.attack_cooldown = 10
        self.attack_range = 20
        self.attack_damage = 10

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -JUMP_STRENGTH
            self.is_jumping = True

    def move(self, direction):
        if direction == "left" and self.rect.x > 0:
            self.rect.x -= self.move_speed
            self.is_moving = True
        elif direction == "right" and self.rect.x < level_width - self.rect.width:
            self.rect.x += self.move_speed
            self.is_moving = True
        else:
            self.is_moving = False

    def attack(self):
        if self.attack_cooldown <= 0:
            self.is_attacking = True
            self.attack_cooldown = 30

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        if self.rect.y >= screen_height - 195:
            self.rect.y = screen_height - 195
            self.is_jumping = False
            self.velocity_y = 0

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        else:
            self.is_attacking = False

    def draw(self, surface):
        health_bar = pygame.Rect(10, 10, 100, 10)
        pygame.draw.rect(surface, BLACK, health_bar)
        pygame.draw.rect(surface, (255, 0, 0), (10, 10, 100, 10), 0)
        pygame.draw.rect(surface, (0, 255, 0), (10, 10, 100 * (self.health / 100), 10), 0)

        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))

        if self.is_attacking:
            attack_rect = pygame.Rect(
                self.rect.x + self.rect.width,
                self.rect.y,
                self.attack_range,
                self.rect.height
            )


class Enemy:
    def __init__(self, x, y):
        self.image = load_image("idle1.png")
        self.image = pygame.transform.scale(self.image, (ENEMY_WIDTH, ENEMY_HEIGHT))
        self.rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.health = 30
        self.max_health = 30
        self.attack_radius = 200
        self.patrol_range = 100
        self.start_x = x
        self.move_speed = 2
        self.patrol_direction = 1

    def update(self, player):
        if self.health <= 0:
            return

        if self.is_in_attack_range(player):
            self.chase_player(player)
        else:
            self.patrol()

        if player.is_attacking:
            attack_rect = pygame.Rect(
                player.rect.x + player.rect.width,
                player.rect.y,
                player.attack_range,
                player.rect.height
            )
            if self.rect.colliderect(attack_rect):
                self.take_damage(player.attack_damage)

    def patrol(self):
        if self.rect.x > self.start_x + self.patrol_range:
            self.patrol_direction = -1
        elif self.rect.x < self.start_x - self.patrol_range:
            self.patrol_direction = 1

        self.rect.x += self.patrol_direction * self.move_speed

    def chase_player(self, player):
        if self.rect.x < player.rect.x:
            self.rect.x += self.move_speed
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.move_speed

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def draw(self, surface):
        if self.health <= 0:
            return

        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))

        health_bar_width = 50
        health_bar_height = 5
        health_bar_x = self.rect.x - camera_x + (self.rect.width - health_bar_width) // 2
        health_bar_y = self.rect.y - 10
        pygame.draw.rect(surface, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (health_bar_x, health_bar_y, health_bar_width * (self.health / self.max_health), health_bar_height))

    def is_in_attack_range(self, player):
        if self.health <= 0:
            return False

        distance = abs(self.rect.x - player.rect.x)
        return distance <= self.attack_radius


player = Player()

enemies = [
    Enemy(1000, screen_height - ENEMY_HEIGHT - 100),
    Enemy(3000, screen_height - ENEMY_HEIGHT - 100),
    Enemy(5000, screen_height - ENEMY_HEIGHT - 100),
    Enemy(7000, screen_height - ENEMY_HEIGHT - 100),
    Enemy(9000, screen_height - ENEMY_HEIGHT - 100)
]

background_img = load_image("city (1).jpg")
background_width = background_img.get_width()

camera_x = 0

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        player.jump()
    if keys[pygame.K_LEFT]:
        player.move("left")
    if keys[pygame.K_RIGHT]:
        player.move("right")
    if keys[pygame.K_a]:
        player.attack()

    player.update()

    if player.rect.x > screen_width - 400 and player.rect.x < level_width - screen_width + 400:
        camera_x = player.rect.x - (screen_width - 400)

    background_offset = camera_x % background_width
    screen.blit(background_img, (-background_offset, 0))
    screen.blit(background_img, (background_width - background_offset, 0))

    for enemy in enemies[:]:
        enemy.update(player)
        enemy.draw(screen)

        if enemy.health <= 0:
            enemies.remove(enemy)

        if enemy.is_in_attack_range(player):
            player.health -= 0.3
    if player.health <= 0:
        print("Game Over!")
        running = False

    player.draw(screen)

    if player.rect.x >= level_width - player.rect.width:
        print("Level Complete!")
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()