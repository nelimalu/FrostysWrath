import pygame
import pygame.gfxdraw
import math
import Helper
import cv2
import numpy as np

background = cv2.imread(r"assets/Background-shadow.png", 0)

GRAPHICS = True


def get_relative_side(obstacle, pos):
    if pos[0] <= obstacle.x and pos[1] <= obstacle.y:
        return "TOP LEFT"
    if pos[0] >= obstacle.x + obstacle.width and pos[1] <= obstacle.y:
        return "TOP RIGHT"
    if pos[0] >= obstacle.x + obstacle.width and pos[1] >= obstacle.y + obstacle.height:
        return "BOTTOM RIGHT"
    if pos[0] <= obstacle.x and pos[1] >= obstacle.y + obstacle.height:
        return "BOTTOM LEFT"

    if pos[0] <= obstacle.x and obstacle.y <= pos[1] < obstacle.y + obstacle.height:
        return "LEFT"
    if pos[0] >= obstacle.x + obstacle.width and obstacle.y <= pos[1] < obstacle.y + obstacle.height:
        return "RIGHT"
    if obstacle.x <= pos[0] < obstacle.x + obstacle.width and pos[1] >= obstacle.y + obstacle.height:
        return "BOTTOM"
    if obstacle.x <= pos[0] < obstacle.x + obstacle.width and pos[1] <= obstacle.y + obstacle.height:
        return "TOP"

    return "TOP"


def get_tripoint(win, points, side):
    if side == "LEFT":
        # 1, 2, 3, 3.5, 4
        points.insert(0, (points[0][0] + win.get_width(), points[0][1]))
        points.append((points[-1][0] + win.get_width(), points[-1][1]))
    if side == "RIGHT":
        points.insert(0, (points[0][0] - win.get_width(), points[0][1]))
        points.append((points[-1][0] - win.get_width(), points[-1][1]))
    if side == "TOP":
        points.insert(0, (points[0][0], points[0][1] + win.get_height()))
        points.append((points[-1][0], points[-1][1] + win.get_height()))
    if side == "BOTTOM":
        points.insert(0, (points[0][0], points[0][1] - win.get_height()))
        points.append((points[-1][0], points[-1][1] - win.get_height()))

    return points


def get_pointslist(win, useful_points, angles):
    pointslist = []
    for x, point in enumerate(useful_points):
        x2 = point[0] + math.sin(angles[x]) * -win.get_width() * 3
        y2 = point[1] + math.cos(angles[x]) * -win.get_height() * 3

        pointslist.append((x2, y2))
        pointslist.append((point[0], point[1]))
    return pointslist


def make_shadow(win, useful_points, angles, side):
    pointslist = get_pointslist(win, useful_points, angles)

    tripoint = get_tripoint(win, [pointslist[0], pointslist[1], pointslist[3], pointslist[2]], side)

    return tripoint, pointslist


class Boulder:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.playerdist = 0
        self.angles = []
        self.useful_points = []
        self.corners = [(x, y), (x + width, y), (x, y + height), (x + width, y + height)]
        self.side = ""
        self.pointslist = [[0, 0], [0, 0], [0, 0], [0, 0]]
        self.pairs = {
            "LEFT": (self.corners[0], self.corners[2]),
            "TOP": (self.corners[0], self.corners[1]),
            "RIGHT": (self.corners[1], self.corners[3]),
            "BOTTOM": (self.corners[2], self.corners[3]),
            "TOP LEFT": (self.corners[1], self.corners[2]),
            "TOP RIGHT": (self.corners[0], self.corners[3]),
            "BOTTOM LEFT": (self.corners[0], self.corners[3]),
            "BOTTOM RIGHT": (self.corners[1], self.corners[2])
        }

    def draw(self, win, player, image):
        self.shadow(win, player)
        # self.draw_shadow(win)
        win.blit(image, (self.x - 10, self.y - 45))

    def draw_shadow(self, win):
        pointslist = [self.pointslist[0], self.pointslist[1], self.pointslist[3], self.pointslist[2]]

        if GRAPHICS:
            mask = np.ones(background.shape, dtype=np.uint8)
            mask.fill(255)

            roi_corners = np.array([pointslist], dtype=np.int32)
            cv2.fillPoly(mask, roi_corners, 0)

            masked_image = cv2.bitwise_or(background, mask)
            cv2.imwrite('assets/new_masked_image.png', masked_image)
            try:
                surf = pygame.image.load('assets/new_masked_image.png')
                surf.set_colorkey((255, 255, 255))
                win.blit(surf, (0, 0))
            except:
                pass
        else:
            pygame.draw.polygon(win, (0,0,0), self.pointslist)

    def shadow(self, win, player):
        self.playerdist = -Helper.get_distance(self.x, self.y, player.x, player.y)
        self.side = get_relative_side(self, (player.x, player.y))
        self.useful_points = self.pairs[self.side]
        self.angles = []
        for point in self.useful_points:
            self.angles.append(Helper.find_angle(point[0], point[1], player.x, player.y))

        if math.degrees(self.angles[0]) == -90.0 and math.degrees(self.angles[1]) > 0 and self.side in ["RIGHT", "TOP RIGHT", "BOTTOM RIGHT"]:
            self.angles[0] = math.radians(90.0)

        if math.degrees(self.angles[1]) == -90.0 and math.degrees(self.angles[0]) > 0 and self.side in ["RIGHT", "TOP RIGHT", "BOTTOM RIGHT"]:
            self.angles[1] = math.radians(90.0)


        # pygame.draw.polygon(win, (22, 22, 22), make_shadow(win, self.useful_points, self.angles, self.side))
        shadow = make_shadow(win, self.useful_points, self.angles, self.side)
        # pygame.gfxdraw.filled_polygon(win, shadow[0], (0, 0, 0, 100))
        self.pointslist = shadow[1]
