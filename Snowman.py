import pygame
import random
import math
import Helper
import Projectiles
import time
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# update
FIRSTSNOWMAN_SPAWN_RATE = 0.01
SECONDSNOWMAN_SPAWN_RATE = 0.008
THIRDSNOWMAN_SPAWN_RATE = 0.005
BORDER = (0, 0, 1100, 650)
SAFE_DISTANCE = 30
TOTAL_SNOWMAN = 5

MATRIX = [[0 for m in range(BORDER[3])] for n in range(BORDER[2])]


def pathfind():
    pass


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

    def draw(self, win, firstsnowman):
        # aidan walking cycle
        pygame.draw.rect(win, (255, 255, 255), (self.x - self.WIDTH // 2, self.y - self.HEIGHT // 2, self.WIDTH, self.HEIGHT))

    def move(self, campfire):
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

class first_snowman(Snowman):

    def shoot(self):
        if self.reached_goal:
            return True

    def move(self, campfire):
        if not self.reached_goal:
            self.x = self.x + math.sin(self.angle) * self.speed
            self.y = self.y + math.cos(self.angle) * self.speed
            if Helper.get_distance(self.x, self.y, campfire.x, campfire.y) <= campfire.FIRE_DISTANCE:
                self.reached_goal = True

    def draw(self, win, firstsnowman):
        if 150 <= self.x <= 900 and (self.y < 250 or self.y > 400):
            if self.y <= 325:
                win.blit(firstsnowman[1], (self.x - self.WIDTH // 2-30, self.y - self.HEIGHT))
            else:
                win.blit(firstsnowman[0], (self.x - self.WIDTH // 2-30, self.y - self.HEIGHT))
        else:
            if self.x <= 550:
                win.blit(firstsnowman[2], (self.x - self.WIDTH // 2-30, self.y - self.HEIGHT))
            else:
                win.blit(firstsnowman[3], (self.x - self.WIDTH // 2-30, self.y - self.HEIGHT))


class second_snowman(Snowman):
    def draw(self, win, secondsnowman):
        if self.x >= 150 and self.x <= 900 and (self.y < 250 or self.y > 400):
            if self.y <= 325:
                win.blit(secondsnowman[1], (self.x - self.WIDTH// 2 - 50, self.y - self.HEIGHT))
            else:
                win.blit(secondsnowman[0], (self.x - self.WIDTH // 2 - 50, self.y - self.HEIGHT))
        else:
            if self.x <= 550:
                win.blit(secondsnowman[2], (self.x - self.WIDTH // 2 - 50, self.y - self.HEIGHT))
            else:
                win.blit(secondsnowman[3], (self.x - self.WIDTH // 2 - 50, self.y - self.HEIGHT))
        #pygame.draw.rect(win, (0, 0, 0), (self.x - self.WIDTH // 2, self.y - self.HEIGHT // 2, self.WIDTH, self.HEIGHT))


class third_snowman(Snowman):
    pass


def get_snowman_location(width, height, border):
    x = random.randint(0, width)
    y = random.randint(0, height)
    while border[1] < y < border[3] and border[0] < x < border[2]:
        y = random.randint(0, height)
        x = random.randint(0, width)

    return x, y


def spawn_firstsnowman(width, height, campfire):
    health = 1
    speed = 2
    damage = 1
    throwing_range = 200
    points = 5
    return first_snowman(get_snowman_location(width, height, campfire.BORDER), campfire, health, speed, damage, throwing_range, points)


def spawn_secondsnowman(width, height, campfire):
    health = 1
    speed = 2
    damage = 3
    throwing_range = 200
    points = 10
    return second_snowman(get_snowman_location(width, height, campfire.BORDER), campfire, health, speed, damage, throwing_range, points)


def spawn_thirdsnowman(width, height, campfire):
    health = 1
    speed = 3
    damage = 6
    throwing_range = 200
    points = 15
    return first_snowman(get_snowman_location(width, height, campfire.BORDER), campfire, health, speed, damage, throwing_range, points)

# MAKE FIREBALLS COLLIDE WITH SNOWMAN
