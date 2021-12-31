import pygame
import random
import math
import Helper
import Projectiles
import time

# update
FIRSTSNOWMAN_SPAWN_RATE = 0.01
SECONDSNOWMAN_SPAWN_RATE = 0.008
THIRDSNOWMAN_SPAWN_RATE = 0.005
BORDER = (0, 0, 1100, 650)
SAFE_DISTANCE = 30
TOTAL_SNOWMAN = 5


class Snowman:
    COOLDOWN = 1
    WIDTH = 25
    HEIGHT = 50
    ANIMATION_RATE = 7

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
        self.shooting = False
        self.animation_step = 0
        self.frame = 0

    def draw(self, win, snowman, snowmanshooting):
        # aidan walking cycle
        pygame.draw.rect(win, (255, 255, 255), (self.x - self.WIDTH // 2, self.y - self.HEIGHT // 2, self.WIDTH, self.HEIGHT))

    def move(self, campfire, boulders):
        x = [self.x][:][0]
        y = [self.y][:][0]

        if not self.reached_goal:
            x = self.x + math.sin(self.angle) * self.speed
            y = self.y + math.cos(self.angle) * self.speed
            if Helper.get_distance(self.x, self.y, self.goal.x, self.goal.y) <= self.throwing_range:
                self.reached_goal = True

        move_x = True
        move_y = True

        rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)
        for boulder in boulders:
            boulder_rect = pygame.Rect((boulder.x - 4, boulder.y - 4, boulder.width + 12, boulder.height + 12))
            if boulder_rect.colliderect(rect):
                if rect.bottom <= boulder_rect.top + 4 or rect.top >= boulder_rect.bottom - 4:
                    move_y = False
                    self.angle = Helper.find_angle(self.x, self.y, self.goal.x, self.goal.y)
                elif rect.left >= boulder_rect.right - 4 or rect.right <= boulder_rect.left + 4:
                    move_x = False
                    self.angle = Helper.find_angle(self.x, self.y, self.goal.x, self.goal.y)

        if move_x:
            self.x = x
        if move_y:
            self.y = y

    def shoot(self):
        if self.reached_goal:
            if time.time() - self.time_since_last_shot >= self.COOLDOWN:
                self.shooting = True
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

    def move(self, campfire, boulders):
        x = [self.x][:][0]
        y = [self.y][:][0]

        if not self.reached_goal:
            x = self.x + math.sin(self.angle) * self.speed
            y = self.y + math.cos(self.angle) * self.speed
            if Helper.get_distance(self.x, self.y, campfire.x, campfire.y) <= campfire.FIRE_DISTANCE:
                self.reached_goal = True

        move_x = True
        move_y = True

        rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)
        for boulder in boulders:
            boulder_rect = pygame.Rect((boulder.x - 4, boulder.y - 4, boulder.width + 12, boulder.height + 12))
            if boulder_rect.colliderect(rect):
                if rect.bottom <= boulder_rect.top - 8 or rect.top >= boulder_rect.bottom - 4:
                    move_y = False
                    self.angle = Helper.find_angle(self.x, self.y, self.goal.x, self.goal.y)
                elif rect.left >= boulder_rect.right - 4 or rect.right <= boulder_rect.left + 4:
                    move_x = False
                    self.angle = Helper.find_angle(self.x, self.y, self.goal.x, self.goal.y)

        if move_x:
            self.x = x
        if move_y:
            self.y = y

    def draw(self, win, firstsnowman, snowmanshooting):
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
    def __init__(self, location, goal, health, speed, damage, throwing_range, points):
        super().__init__(location, goal, health, speed, damage, throwing_range, points)
        self.WIDTH = 40
        self.HEIGHT = 80

    def draw(self, win, secondsnowman, secondsnowmanshooting):
        self.frame += 1

        if self.frame % (self.ANIMATION_RATE * 3) == 0:
            if self.shooting:
                self.shooting = False

        if self.shooting:
            if self.y <= 200:
                win.blit(secondsnowmanshooting[1], (self.x - self.WIDTH// 2 - 50, self.y - self.HEIGHT))
            elif self.y >= 450:
                win.blit(secondsnowmanshooting[0], (self.x - self.WIDTH// 2 - 50, self.y - self.HEIGHT))
            elif self.x <= 450:
                win.blit(secondsnowmanshooting[2], (self.x - self.WIDTH// 2 - 50, self.y - self.HEIGHT))
            else:
                win.blit(secondsnowmanshooting[3], (self.x - self.WIDTH// 2 - 50, self.y - self.HEIGHT))

        else:
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
    def __init__(self, location, goal, health, speed, damage, throwing_range, points):
        super().__init__(location, goal, health, speed, damage, throwing_range, points)
        self.WIDTH = 60
        self.HEIGHT = 120

    def move(self, campfire, boulders):
        x = [self.x][:][0]
        y = [self.y][:][0]

        if not self.reached_goal:
            x = self.x + math.sin(self.angle) * self.speed
            y = self.y + math.cos(self.angle) * self.speed
            if Helper.get_distance(self.x, self.y, campfire.x, campfire.y) <= campfire.FIRE_DISTANCE:
                self.reached_goal = True

        move_x = True
        move_y = True

        rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)
        for boulder in boulders:
            boulder_rect = pygame.Rect((boulder.x - 4, boulder.y - 4, boulder.width + 12, boulder.height + 12))
            if boulder_rect.colliderect(rect):
                if rect.bottom <= boulder_rect.top - 8 or rect.top >= boulder_rect.bottom - 4:
                    move_y = False
                    self.angle = Helper.find_angle(self.x, self.y, self.goal.x, self.goal.y)
                elif rect.left >= boulder_rect.right - 4 or rect.right <= boulder_rect.left + 4:
                    move_x = False
                    self.angle = Helper.find_angle(self.x, self.y, self.goal.x, self.goal.y)

        if move_x:
            self.x = x
        if move_y:
            self.y = y

    def draw(self, win, thirdsnowman, thirdsnowmanshooting):
        self.frame += 1

        if self.frame % (self.ANIMATION_RATE * 3) == 0:
            if self.shooting:
                self.shooting = False

        if self.shooting:
            if self.y <= 200:
                win.blit(thirdsnowmanshooting[1], (self.x - self.WIDTH// 2 - 70, self.y - self.HEIGHT))
            elif self.y >= 450:
                win.blit(thirdsnowmanshooting[0], (self.x - self.WIDTH// 2 - 70, self.y - self.HEIGHT))
            elif self.x <= 450:
                win.blit(thirdsnowmanshooting[2], (self.x - self.WIDTH// 2 - 70, self.y - self.HEIGHT))
            else:
                win.blit(thirdsnowmanshooting[3], (self.x - self.WIDTH// 2 - 70, self.y - self.HEIGHT))

        else:
            if self.x >= 150 and self.x <= 900 and (self.y < 250 or self.y > 400):
                if self.y <= 325:
                    win.blit(thirdsnowman[1], (self.x - self.WIDTH// 2 - 70, self.y - self.HEIGHT))
                else:
                    win.blit(thirdsnowman[0], (self.x - self.WIDTH // 2 - 70, self.y - self.HEIGHT))
            else:
                if self.x <= 550:
                    win.blit(thirdsnowman[2], (self.x - self.WIDTH // 2 - 70, self.y - self.HEIGHT))
                else:
                    win.blit(thirdsnowman[3], (self.x - self.WIDTH // 2 - 70, self.y - self.HEIGHT))
        #pygame.draw.rect(win, (0, 0, 0), (self.x - self.WIDTH // 2, self.y - self.HEIGHT // 2, self.WIDTH, self.HEIGHT))



def get_snowman_location(width, height, border):
    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)
    while border[1] < y < border[3] and border[0] < x < border[2]:
        y = random.randint(0, height - 1)
        x = random.randint(0, width - 1)

    return x, y


def spawn_firstsnowman(width, height, campfire):
    health = 1
    speed = 2
    damage = 1
    throwing_range = 200
    points = 5
    return first_snowman(get_snowman_location(width, height, campfire.BORDER), campfire, health, speed, damage, throwing_range, points)


def spawn_secondsnowman(width, height, campfire):
    health = 7
    speed = 2
    damage = 3
    throwing_range = 200
    points = 10
    return second_snowman(get_snowman_location(width, height, campfire.BORDER), campfire, health, speed, damage, throwing_range, points)


def spawn_thirdsnowman(width, height, campfire):
    health = 100
    speed = 2
    damage = 6
    throwing_range = 200
    points = 15
    return third_snowman(get_snowman_location(width, height, campfire.BORDER), campfire, health, speed, damage, throwing_range, points)

# MAKE FIREBALLS COLLIDE WITH SNOWMAN
