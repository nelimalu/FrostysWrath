import math


def get_distance(x1, y1, x2, y2):
    return math.sqrt((abs(x2 - x1) ** 2) + (abs(y2 - y1) ** 2))


def collide(x1, y1, w1, h1, x2, y2):
    return x1 <= x2 <= x1 + w1 and y1 <= y2 <= y1 + h1


def find_angle(x1, y1, x2, y2):
    try:
        angle = math.atan((y2 - y1) / (x2 - x1))
        # this tries to get the angle from the ground and the angle made by the mouse
    except ArithmeticError:
        angle = math.pi / 2
        # if the above doesnt work then the result HAS to be this. this is because of unit circle

    if y1 < y2 and x1 > x2:
        angle = abs(angle)
    elif y1 < y2 and x1 < x2:
        angle = math.pi - angle
    elif y1 > y2 and x1 < x2:
        angle = math.pi + abs(angle)
    elif y1 > y2 and x1 > x2:
        angle = (math.pi * 2) - angle

    # this chunk just figures out which quadrant you're shooting in
    # remember in a graph with four quadrants, ball is 0,0

    return angle - math.radians(90)

