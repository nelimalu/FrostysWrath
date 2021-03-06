import pygame
import pygame.gfxdraw
import random
import Helper


class Campfire:
    FREEZE_DISTANCE = 175
    GAIN_DISTANCE = 100
    FIRE_DISTANCE = 85
    WOOD_SPAWN_RATE = 0.005
    BORDER = (125, 100, 1000, 550)
    MAX_AMOUNT = 5
    ANIMATION_RATE = 5

    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.bar_length = 100
        self.ratio = self.max_health/self.bar_length
        self.wood = []
        self.animation_step = 0
        self.frame = 0

    def draw(self, win, campfires):
        self.frame += 1
        if self.frame % self.ANIMATION_RATE == 0:
            self.animation_step += 1
        if self.animation_step == 3:
            self.animation_step = 0

        pygame.gfxdraw.aacircle(win, self.x, self.y, self.FREEZE_DISTANCE, (100,100,100))
        # pygame.gfxdraw.aacircle(win, self.x, self.y, self.GAIN_DISTANCE, (0, 255, 0))

        # Campfire
        # pygame.draw.circle(win, (255, 255, 0), (self.x, self.y), self.FIRE_DISTANCE, 1)
        win.blit(campfires[self.animation_step], (self.x - 70, self.y - 70))

        # Health Bar
        pygame.draw.rect(win, (0,255,0), (self.x-50, self.y+70,self.health/self.ratio,15))
        pygame.draw.rect(win, (0,0,0), (self.x-50, self.y+70,self.bar_length,15),4)

        # Border
        # pygame.draw.rect(win, (255,0,255), (self.BORDER[0], self.BORDER[1], self.BORDER[2] - self.BORDER[0], self.BORDER[3] - self.BORDER[1]), 3)

    def get_wood_location(self):
        x = random.randint(self.BORDER[0], self.BORDER[2])
        y = random.randint(self.BORDER[1], self.BORDER[3])
        while Helper.get_distance(x, y, self.x, self.y) <= self.FREEZE_DISTANCE:
            x = random.randint(self.BORDER[0], self.BORDER[2])
            y = random.randint(self.BORDER[1], self.BORDER[3])
        return x, y

    def spawn_wood(self):
        if random.random() < self.WOOD_SPAWN_RATE and len(self.wood) < self.MAX_AMOUNT:
            self.wood.append(Wood(self.get_wood_location()))

    def take_damage(self, damage):
        if self.health > 0:
            self.health -= damage

    def gain_health(self, amount):
        if self.health < self.max_health:
            self.health += amount


class Wood:
    HEAL_AMOUNT = 30

    def __init__(self, location):
        self.x = location[0]
        self.y = location[1]
        self.width = 25
        self.height = 25

    def draw(self, win, wood):
        # pygame.draw.rect(win, (150, 75, 0), (self.x - self.width, self.y - self.height, self.width, self.height))
        win.blit(wood, (self.x - self.width, self.y - self.height))
