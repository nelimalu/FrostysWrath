import math


def get_distance(x1, y1, x2, y2):
    return math.sqrt((abs(x2 - x1) ** 2) + (abs(y2 - y1) ** 2))


def collide(x1, y1, w1, h1, x2, y2):
    return x1 < x2 < x1 + w1 and y1 < y2 < y1 + h1
