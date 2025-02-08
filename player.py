import pygame
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COIN_COLOR = (255, 223, 0)

GRAVITY = 1
JUMP_STRENGTH = 15
ENEMY_WIDTH = 140
ENEMY_HEIGHT = 140

screen_width = 1500
screen_height = 700
level_width = 5500


class Player:
    def __init__(self):
        self.idle_frames = self.load_images_from_folder("idle")
        self.run_frames = self.load_images_from_folder("run")
        self.jump_frames = self.load_images_from_folder("jump")
        self.attack_frames = self.load_images_from_folder("attack")

        self.current_frame = 0
        self.animation_speed = 1.5
        self.last_update = pygame.time.get_ticks()

        self.state = "idle"
        self.image = self.idle_frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(50, screen_height - 200))

        self.velocity_y = 0
        self.is_jumping = False
        self.move_speed = 5
        self.health = 100
        self.is_attacking = False
        self.attack_cooldown = 40
        self.attack_range = 50
        self.attack_damage = 0.33
        self.score = 0
        self.facing_right = True

    def attack(self):
        if self.attack_cooldown <= 0:
            self.is_attacking = True
            self.attack_cooldown = 60
            self.state = "attack"

    def is_facing_enemy(self, enemy):
        if self.facing_right and enemy.rect.x > self.rect.x:
            return True
        elif not self.facing_right and enemy.rect.x < self.rect.x:
            return True
        return False

    def is_in_attack_range(self, enemy):
        distance = abs(self.rect.x - enemy.rect.x)
        return distance <= self.attack_range

    def load_images_from_folder(self, folder):
        frames = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(".png"):
                image = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
                image = pygame.transform.scale(image, (120, 140))
                frames.append(image)
        return frames

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 1000 // (len(self.get_current_frames()) * self.animation_speed):
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.get_current_frames())
            self.image = self.get_current_frames()[self.current_frame]

    def get_current_frames(self):
        if self.state == "idle":
            return self.idle_frames
        elif self.state == "run":
            return self.run_frames
        elif self.state == "jump":
            return self.jump_frames
        elif self.state == "attack":
            return self.attack_frames
        return self.idle_frames

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -JUMP_STRENGTH
            self.is_jumping = True
            self.state = "jump"

    def move(self, direction):
        if direction == "left" and self.rect.x > 0:
            self.rect.x -= self.move_speed
            self.state = "run"
            self.facing_right = False
        elif direction == "right" and self.rect.x < level_width - self.rect.width:
            self.rect.x += self.move_speed
            self.state = "run"
            self.facing_right = True
        else:
            if not self.is_jumping and not self.is_attacking:
                self.state = "idle"

    def attack(self):
        if self.attack_cooldown <= 0:
            self.is_attacking = True
            self.attack_cooldown = 60
            self.state = "attack"

    def update(self):
        self.animate()

        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        if self.rect.y >= screen_height - 195:
            self.rect.y = screen_height - 195
            self.is_jumping = False
            self.velocity_y = 0
            if not self.is_attacking:
                self.state = "idle"

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        else:
            self.is_attacking = False
            if not self.is_jumping:
                self.state = "idle"

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
        if not self.facing_right:
            flipped_image = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_image, (self.rect.x - camera_x, self.rect.y))
        else:
            surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))