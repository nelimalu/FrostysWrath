import pygame
import Projectiles


class Player:
    FIRE_REGEN_RATE = 1  # regenerate 1 fireball per second
    WIDTH = 50
    HEIGHT = 50

    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.fireballs = 0  # how many fireballs the player has
        self.health = 100

    def draw(self, win):
        pygame.draw.rect(win, (0,0,0), (self.x - (self.WIDTH // 2), self.y - (self.HEIGHT // 2), self.WIDTH, self.HEIGHT))

    def move(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed

    def shoot(self, endpos):
        # run animation here
        return Projectiles.Fireball(self.x, self.y, endpos, 1, 1, 5)
