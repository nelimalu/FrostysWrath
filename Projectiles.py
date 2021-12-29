import pygame
import pygame.gfxdraw
import math

GRAVITY = 0.01
BOUNDS_MARGIN = 30


def find_angle(x1, y1, x2, y2):
    try:
        angle = math.atan((y2 - y1) / (x2 - x1))
        # this tries to get the angle from the ground and the angle made by the mouse
    except ArithmeticError:
        angle = math.pi / 2
        # if the above doesnt work then the result HAS to be this. this is because of unit circle

    if y1 < y2 and x1 > x2:
        angle = abs(angle)
    elif y1 < y2 and x1 < x2:
        angle = math.pi - angle
    elif y1 > y2 and x1 < x2:
        angle = math.pi + abs(angle)
    elif y1 > y2 and x1 > x2:
        angle = (math.pi * 2) - angle

    # this chunk just figures out which quadrant you're shooting in
    # remember in a graph with four quadrants, ball is 0,0

    return angle - math.radians(90)


class Projectile:
    def __init__(self, x, y, endpos, speed, damage, size):
        self.x = x
        self.y = y
        self.endpos = endpos  # the projectile's ideal ending position
        self.angle = find_angle(x, y, endpos[0], endpos[1])
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
    def __init__(self, x, y, endpos, speed, damage, size):
        super().__init__(x, y, endpos, speed, damage, size)
        self.airtime = 0  # the amount of the time snowball been in the air

    def move(self):
        self.airtime += 1
        self.x = self.x + math.sin(self.angle) * self.speed
        self.y = self.y + (math.cos(self.angle) * self.speed) + (self.airtime * GRAVITY)  # fake arc for snowball


class Fireball(Projectile):
    pass
