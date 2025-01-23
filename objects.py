import pygame


class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load("idle1.png")
        self.image = pygame.transform.scale(self.image, (140, 140))
        self.rect = pygame.Rect(x, y, 140, 140)
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

    def draw(self, surface, camera_x):
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


class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)

    def draw(self, surface, camera_x):
        pygame.draw.rect(surface, (0, 0, 255), (self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height))


class Pit:
    def __init__(self, x, y, width, height):
        self.image = pygame.image.load("pit.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)

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


class Spike:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface, camera_x):
        pygame.draw.polygon(surface, (255, 0, 0), [
            (self.rect.x - camera_x + self.rect.width // 2, self.rect.y),
            (self.rect.x - camera_x, self.rect.y + self.rect.height),
            (self.rect.x - camera_x + self.rect.width, self.rect.y + self.rect.height)
        ])
