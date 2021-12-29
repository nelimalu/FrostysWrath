import pygame
import pygame.gfxdraw
import Projectiles
import Helper
import time


class Player:
    FIRE_REGEN_RATE = 1  # regenerate 1 fireball per second
    MAX_FIREBALLS = 5
    FREEZE_SPEED = 0.1
    WIDTH = 25
    HEIGHT = 25

    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.fireballs = 3  # how many fireballs the player has
        self.freezing = False
        self.time_freezing = 0
        self.max_fireball = 5
        self.time_gaining = 0
        self.bar_length = 500
        self.ratio = self.max_fireball/self.bar_length

    def draw(self, win):
        pygame.draw.rect(win, (0,0,0), (self.x - (self.WIDTH // 2), self.y - (self.HEIGHT // 2), self.WIDTH, self.HEIGHT))

    def draw_freezing(self, win, width, height):
        if 250 > self.time_freezing > 0:
            pygame.gfxdraw.filled_polygon(win, ((0, 0), (0, height), (width, height), (width, 0)), (0, 191, 255, self.time_freezing))

    def check_freezing(self, campfire):
        if Helper.get_distance(self.x, self.y, campfire.x, campfire.y) > campfire.FREEZE_DISTANCE:
            self.time_freezing += self.FREEZE_SPEED
        else:
            self.time_freezing = self.time_freezing - self.FREEZE_SPEED if self.time_freezing > 0 else 0

    def check_gain(self, campfire):
        if Helper.get_distance(self.x, self.y, campfire.x, campfire.y) < campfire.GAIN_DISTANCE:
            if self.time_gaining == 0:
                self.time_gaining = time.time()
            elif time.time() - self.time_gaining >= self.FIRE_REGEN_RATE:
                self.fireballs += 1 if self.fireballs < self.MAX_FIREBALLS else 0
                self.time_gaining = time.time()

    def update(self, keys, campfire):
        self.move(keys)
        self.check_freezing(campfire)
        self.check_gain(campfire)

    def move(self, keys):
        speed = self.speed - (self.time_freezing * 0.1)
        if speed < 1:
            speed = 1

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += speed

    def draw_fireball_bar(self, win, width):
        pygame.draw.rect(win, (255,165,0), (width//2-250, 600,self.fireballs/self.ratio,25))
        pygame.draw.rect(win, (0,0,0), (width//2-250, 600,self.bar_length,25),5)

    def shoot(self, endpos):
        if self.fireballs > 0:
            self.fireballs -= 1
            return Projectiles.Fireball(self.x, self.y, endpos, 6, 1, 5)
