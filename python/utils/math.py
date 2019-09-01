import math


def clamp(num, range_min, range_max):
    return max(min(num, range_max), range_min)


def sq_dist(x1: float, y1: float, x2: float, y2: float) -> float:
    return (x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1)


def dist(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt(sq_dist(x1, y1, x2, y2))
