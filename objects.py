import pygame
import os


class Enemy:
    def __init__(self, x, y):
        self.run_frames = self.load_images_from_folder("enemy_run")
        self.start_x = x
        self.current_frame = 0
        self.animation_speed = 1.2
        self.last_update = pygame.time.get_ticks()

        self.image = self.run_frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 1.0
        self.max_health = 1.0
        self.attack_radius = 200
        self.patrol_range = 100
        self.move_speed = 2
        self.patrol_direction = 1
        self.facing_right = True

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0


    def load_images_from_folder(self, folder):
        frames = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(".png"):
                image = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
                image = pygame.transform.scale(image, (120, 120))
                frames.append(image)
        return frames

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 1000 // (len(self.get_current_frames()) * self.animation_speed):
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.get_current_frames())
            self.image = self.get_current_frames()[self.current_frame]

    def get_current_frames(self):
        return self.run_frames

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

        self.animate()

    def patrol(self):
        if self.rect.x > self.start_x + self.patrol_range:
            self.patrol_direction = -1
            self.facing_right = False
        elif self.rect.x < self.start_x - self.patrol_range:
            self.patrol_direction = 1
            self.facing_right = True
        self.rect.x += self.patrol_direction * self.move_speed

    def chase_player(self, player):
        if self.rect.x < player.rect.x:
            self.rect.x += self.move_speed
            self.facing_right = True
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.move_speed
            self.facing_right = False

    def draw(self, surface, camera_x):
        if self.health <= 0:
            return
        if not self.facing_right:
            flipped_image = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_image, (self.rect.x - camera_x, self.rect.y))
        else:
            surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))

    def is_in_attack_range(self, player):
        if player.rect.y + player.rect.height <= self.rect.y:
            return
        if self.health <= 0:
            return False

        distance = abs(self.rect.x - player.rect.x)
        return distance <= self.attack_radius


class Obstacle:
    def __init__(self, x, y, obstacle_type, width=60, height=60):
        self.obstacle_type = obstacle_type
        self.image = self.load_image(obstacle_type)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

    def load_image(self, obstacle_type):
        if obstacle_type == "trashbin":
            return pygame.image.load("trashbin (1).png").convert_alpha()
        elif obstacle_type == "wall":
            return pygame.image.load("wall (1).png").convert_alpha()
        elif obstacle_type == "manhole":
            return pygame.image.load("manhole(1).png").convert_alpha()
        elif obstacle_type == "barrel":
            return pygame.image.load("barrel (1).png").convert_alpha()
        elif obstacle_type == "log":
            return pygame.image.load("log.png").convert_alpha()

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))


class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface, camera_x):
        pygame.draw.rect(surface, (0, 128, 0), (self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height))


class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.collected = False

    def draw(self, surface, camera_x):
        if not self.collected:
            pygame.draw.ellipse(surface, (255, 223, 0), (self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height))

