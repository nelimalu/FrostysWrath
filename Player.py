import pygame
import pygame.gfxdraw
import Projectiles
import Helper
import time

# update


class Player:
    FIRE_REGEN_RATE = 1  # regenerate 1 fireball per second
    MAX_FIREBALLS = 10
    FREEZE_SPEED = 0.5
    WIDTH = 100
    HEIGHT = 100
    ANIMATION_RATE = 7

    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.fireballs = self.MAX_FIREBALLS  # how many fireballs the player has
        self.freezing = False
        self.time_freezing = 0
        self.time_gaining = 0
        self.bar_length = 500
        self.ratio = self.MAX_FIREBALLS / self.bar_length
        self.animation_step_side = 0
        self.animation_step = 0
        self.frame = 0
        self.direction = "front"
        self.shooting = False

    def draw(self, win, keys, mousepos, right, left, front, back, shoot):
        self.frame += 1
        if self.frame % self.ANIMATION_RATE == 0:
            self.animation_step_side += 1
            self.animation_step += 1
        if self.frame % (self.ANIMATION_RATE*3) == 0:
            if self.shooting:
                self.shooting = False
        if self.animation_step_side == 2:
            self.animation_step_side = 0
        if self.animation_step == 3:
            self.animation_step = 0

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.shooting:
                win.blit(shoot[0], (self.x - 70, self.y - 70))
            else:
                win.blit(right[self.animation_step_side], (self.x - 70, self.y - 70))
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.shooting:
                win.blit(shoot[1], (self.x - 70, self.y - 70))
            else:
                win.blit(left[self.animation_step_side], (self.x - 70, self.y - 70))
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if self.shooting:
                win.blit(shoot[2], (self.x - 70, self.y - 70))
            else:
                win.blit(front[self.animation_step], (self.x - 70, self.y - 70))
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.shooting:
                win.blit(shoot[3], (self.x - 70, self.y - 70))
            else:
                win.blit(back[self.animation_step], (self.x - 70, self.y - 70))
        else:
            if self.shooting:
                if mousepos[1] >= self.y-30 and mousepos[1] <= self.y-30 + self.HEIGHT:
                    if mousepos[0] >= self.x+self.WIDTH:
                        win.blit(shoot[0], (self.x - 70, self.y - 70))
                    elif mousepos[0] <= self.x:
                        win.blit(shoot[1], (self.x - 70, self.y - 70))
                else:
                    if mousepos[1] > self.y-30+self.HEIGHT:
                        win.blit(shoot[2], (self.x - 70, self.y - 70))
                    elif mousepos[1] < self.y-30:
                        win.blit(shoot[3], (self.x - 70, self.y - 70))
            else:
                if self.direction == "right":
                        win.blit(right[0], (self.x - 70, self.y - 70))
                elif self.direction == "left":
                        win.blit(left[0], (self.x - 70, self.y - 70))
                elif self.direction == "front":
                        win.blit(front[0], (self.x - 70, self.y - 70))
                else:
                        win.blit(back[0], (self.x - 70, self.y - 70))

    def draw_freezing(self, win, image):
        if 250 > self.time_freezing > 0:
            image.set_alpha(self.time_freezing)
            win.blit(image, (0, 0))
            # pygame.gfxdraw.filled_polygon(win, ((0, 0), (0, height), (width, height), (width, 0)), (0, 191, 255, self.time_freezing))

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
        self.move(keys, campfire)
        self.check_freezing(campfire)
        self.check_gain(campfire)

    def move(self, keys, campfire):
        speed = self.speed - (self.time_freezing * 0.1)
        if speed < 1:
            speed = 1

        x = [self.x][:][0]
        y = [self.y][:][0]

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            y -= speed
            self.direction = "back"
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            y += speed
            self.direction = "front"
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            x -= speed
            self.direction = "left"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            x += speed
            self.direction = "right"

        if Helper.get_distance(self.x, y, campfire.x, campfire.y) >= campfire.FIRE_DISTANCE:
            self.y = y
        if Helper.get_distance(x, self.y, campfire.x, campfire.y) >= campfire.FIRE_DISTANCE:
            self.x = x

        self.validate_move(campfire.BORDER)

    def validate_move(self, border):
        if self.x - self.WIDTH // 2 < border[0]:
            self.x = border[0] + self.WIDTH // 2
        elif self.x + self.WIDTH // 2 > border[2]:
            self.x = border[2] - self.WIDTH // 2
        if self.y - self.HEIGHT // 2 < border[1]:
            self.y = border[1] + self.HEIGHT // 2
        elif self.y + self.HEIGHT // 2 > border[3]:
            self.y = border[3] - self.HEIGHT // 2

    def draw_fireball_bar(self, win, width):
        pygame.draw.rect(win, (255,165,0), (width//2-250, 600,self.fireballs/self.ratio,25))
        pygame.draw.rect(win, (0,0,0), (width//2-250, 600,self.bar_length,25),5)

    def shoot(self, endpos):
        if self.fireballs > 0:
            self.fireballs -= 1
            speed = 8
            damage = 15
            self.shooting = True
            size = 5
            return Projectiles.Fireball(self.x, self.y, endpos, speed, damage, size)
