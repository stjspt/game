import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 128, 255)
ENEMY_COLOR = (0, 255, 0)
OBSTACLE_COLOR = (0, 0, 255)
COIN_COLOR = (255, 223, 0)
SPIKE_COLOR = (255, 0, 0)

GRAVITY = 1
JUMP_STRENGTH = 15
ENEMY_WIDTH = 140
ENEMY_HEIGHT = 140

screen_width = 1500
screen_height = 700
level_width = 1000

class Player:
    def __init__(self):
        self.image = pygame.image.load("idle.png")
        self.image = pygame.transform.scale(self.image, (120, 140))
        self.rect = pygame.Rect(50, screen_height - 200, 120, 140)
        self.velocity_y = 0
        self.is_jumping = False
        self.move_speed = 5
        self.health = 100
        self.is_attacking = False
        self.attack_cooldown = 10
        self.attack_range = 20
        self.attack_damage = 10
        self.score = 0

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

    def check_collision_with_obstacles(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if self.is_jumping:
                    continue
                if self.rect.x < obstacle.rect.x:
                    self.rect.x = obstacle.rect.x - self.rect.width
                else:
                    self.rect.x = obstacle.rect.x + obstacle.rect.width

    def draw(self, surface, camera_x):
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
