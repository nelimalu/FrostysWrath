import pygame
import pygame.gfxdraw
import math
import Helper

GRAVITY = 0.01
BOUNDS_MARGIN = 30

# update


class Projectile:
    def __init__(self, x, y, endpos, speed, damage, size):
        self.x = x
        self.y = y
        self.endpos = endpos  # the projectile's ideal ending position
        self.angle = Helper.find_angle(x, y, endpos[0], endpos[1])
        self.speed = speed
        self.damage = damage
        self.size = size

    def draw(self, win):
        pygame.gfxdraw.aacircle(win, int(self.x), int(self.y), self.size, (0,0,0))

    def move(self):
        # move the snowball along an angle
        self.x += math.sin(self.angle) * self.speed
        self.y += math.cos(self.angle) * self.speed

    def is_out_of_bounds(self, width, height):
        return -BOUNDS_MARGIN > self.x or self.x > width + BOUNDS_MARGIN or -BOUNDS_MARGIN > self.y or self.y > height + BOUNDS_MARGIN


class Snowball(Projectile):
    def __init__(self, x, y, endpos, speed, damage, size, goal):
        super().__init__(x, y, endpos, speed, damage, size)
        self.airtime = 0  # the amount of the time snowball been in the air
        self.goal = goal

    def move(self):
        self.airtime += 1
        self.x = self.x + math.sin(self.angle) * self.speed
        self.y = self.y + (math.cos(self.angle) * self.speed) + (self.airtime * GRAVITY)  # fake arc for snowball

    def hit_goal(self):
        return Helper.get_distance(self.x, self.y, self.goal.x, self.goal.y) < self.speed + 1


class Fireball(Projectile):
    def hit_snowman(self, snowmen):
        for snowman in snowmen:
            x = snowman.x - (snowman.WIDTH // 2)
            y = snowman.y - (snowman.HEIGHT // 2)
            if Helper.collide(x, y, snowman.WIDTH, snowman.HEIGHT, self.x, self.y):
                return snowman
