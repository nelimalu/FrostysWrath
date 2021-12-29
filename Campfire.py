import pygame


class Campfire:
    FREEZE_DISTANCE = 250
    GAIN_DISTANCE = 50

    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health

    def draw(self, win):
        pygame.draw.circle(win, (255,0,0), (self.x, self.y), self.FREEZE_DISTANCE, 1)
        pygame.draw.circle(win, (0, 255, 0), (self.x, self.y), self.GAIN_DISTANCE, 1)
        pygame.draw.circle(win, (255,255,0), (self.x, self.y), 30)
