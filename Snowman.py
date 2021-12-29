import pygame
import random
import math
import Helper
import Projectiles
import time

# update

SNOWMAN_SPAWN_RATE = 0.01
BORDER = (0, 0, 1100, 650)
SAFE_DISTANCE = 30


class Snowman:
    COOLDOWN = 1
    WIDTH = 25
    HEIGHT = 50

    def __init__(self, location, goal, health, speed, damage, throwing_range, points):
        self.x = location[0]
        self.y = location[1]
        self.goal = goal
        self.health = health
        self.speed = speed
        self.damage = damage
        self.throwing_range = throwing_range
        self.angle = Helper.find_angle(self.x, self.y, goal.x, goal.y)
        self.reached_goal = False
        self.time_since_last_shot = 0
        self.points = points

    def draw(self, win):
        # aidan walking cycle
        pygame.draw.rect(win, (255, 255, 255), (self.x - self.WIDTH // 2, self.y - self.HEIGHT // 2, self.WIDTH, self.HEIGHT))

    def move(self):
        if not self.reached_goal:
            self.x = self.x + math.sin(self.angle) * self.speed
            self.y = self.y + math.cos(self.angle) * self.speed
            if Helper.get_distance(self.x, self.y, self.goal.x, self.goal.y) <= self.throwing_range:
                self.reached_goal = True

    def shoot(self):
        if self.reached_goal:
            if time.time() - self.time_since_last_shot >= self.COOLDOWN:
                self.time_since_last_shot = time.time()
                return Projectiles.Snowball(self.x, self.y, (self.goal.x, self.goal.y), 6, 1, 5, self.goal)

    def take_damage(self, damage):
        self.health -= damage

    def is_dead(self):
        return self.health <= 0


def get_snowman_location(width, height, border):
    x = random.randint(0, width)
    y = random.randint(0, height)
    while border[1] < y < border[3] and border[0] < x < border[2]:
        y = random.randint(0, height)
        x = random.randint(0, width)

    return x, y


def spawn_snowman(width, height, campfire):
    health = 10
    speed = 2
    damage = 1
    throwing_range = 200
    points = 5
    return Snowman(get_snowman_location(width, height, campfire.BORDER), campfire, health, speed, damage, throwing_range, points)

# MAKE FIREBALLS COLLIDE WITH SNOWMAN
