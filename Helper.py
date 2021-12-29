import math


def get_distance(x1, y1, x2, y2):
    return math.sqrt((abs(x2 - x1) ** 2) + (abs(y2 - y1) ** 2))