import pygame


class Campfire:
    FREEZE_DISTANCE = 175
    GAIN_DISTANCE = 50

    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.bar_length = 100
        self.ratio = self.max_health/self.bar_length

    def draw(self, win):
        pygame.draw.circle(win, (255,0,0), (self.x, self.y), self.FREEZE_DISTANCE, 1)
        pygame.draw.circle(win, (0, 255, 0), (self.x, self.y), self.GAIN_DISTANCE, 1)
        pygame.draw.circle(win, (255,255,0), (self.x, self.y), 30)
        pygame.draw.rect(win, (0,255,0), (self.x-50, self.y+50,self.health/self.ratio,15))
        pygame.draw.rect(win, (0,0,0), (self.x-50, self.y+50,self.bar_length,15),4)

    def take_damage(self, damage):
        if self.health > 0:
            self.health -= damage

    def gain_health(self, amount):
        if self.health < self.max_health:
            self.health += amount
