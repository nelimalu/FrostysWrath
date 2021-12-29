import pygame
import random
import Helper

class Snowmen:
    SNOWMAN_SPAWN_RATE = 0.01
    BORDER = (0, 0, 1100, 650)
    SAFE_DISTANCE = 30

    def __init__(self, location, health, speed, damage):
        self.x = location[0]
        self.y = location[1]
        self.width = 25
        self.height = 50
        self.health = health
        self.speed = speed
        self.damage = damage
        self.snowmans = []

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), (self.x - self.width, self.y - self.height, self.width, self.height))

    def get_snowman_location(self):
        x = random.randint(self.BORDER[0], self.BORDER[2])
        y = random.randint(self.BORDER[1], self.BORDER[3])
        while y >= 100 and y <= 550:
            y = random.randint(self.BORDER[1], self.BORDER[3])
        while x >= 100 and x <= 1000:
            x = random.randint(self.BORDER[0], self.BORDER[2])
        return x, y

    def spawn_snowman(self):
        if random.random() < self.SNOWMAN_SPAWN_RATE:
            self.snowmans.append(Snowmen(self.get_snowman_location(), 10, 5, 2))

    def take_damage(self):
        pass