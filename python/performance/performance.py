from dataclasses import dataclass, replace
from typing import List, Tuple
from time import time
import random


"""
Some performance profiling of different styles of Python code. The goal is to
profile the best way to represent a Point(x, y) which we must frequently
update.

The options are:

1. Use a tuple, and create a new tuple with each update.
2. Use a class, and mutate the instance for each update.
3. Use a class, and construct a new instance for each update.
4. Use a dataclass, and use `replace` to construct a new instance for each
update
5. Use a dataclass, and manually construct a new instance for each update
5. Use a dataclass, and mutate the instance for each update


The performance of each of these options (in seconds, so large numbers are
bad):

1. profile_tuple: 0.14
2. profile_point0: 0.18
3. profile_point1: 0.35
4. profile_point_class0: 1.08
5. profile_point_class1: 0.36
6. profile_point_class2: 0.18

Given the cleaner syntax of dataclasses, and equivalent performance, we
recommend using dataclasses wherever possible. However, whether to mutate them
or construct new instances is up to you (if the tradeoff of using mutability is
worth the ~2x performance gain).
"""

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


@dataclass
class DataPoint:
    x: int
    y: int


def profile_point0(initial: Tuple[int, int], values: List[Tuple[int, int]]):
    point = Point(initial[0], initial[1])
    for (x0, y0) in values:
        point.x = x0
        point.y = y0

def profile_point1(initial: Tuple[int, int], values: List[Tuple[int, int]]):
    point = Point(initial[0], initial[1])
    for (x0, y0) in values:
        point = Point(x0, y0)

def profile_point_dataclass0(initial: Tuple[int, int], values: List[Tuple[int, int]]):
    point = DataPoint(initial[0], initial[1])
    for (x0, y0) in values:
        point = replace(point, x=x0, y=y0)

def profile_point_dataclass1(initial: Tuple[int, int], values: List[Tuple[int, int]]):
    point = DataPoint(initial[0], initial[1])
    for (x0, y0) in values:
        point = DataPoint(x0, y0)

def profile_point_dataclass2(initial: Tuple[int, int], values: List[Tuple[int, int]]):
    point = DataPoint(initial[0], initial[1])
    for (x0, y0) in values:
        point.x = x0
        point.y = y0

def profile_tuple(initial: Tuple[int, int], values: List[Tuple[int, int]]):
    tup = initial
    for (x0, y0) in values:
        tup = (x0, y0)


if __name__ == "__main__":
    xs = random.sample(range(round(1e6)), round(1e6))
    ys = random.sample(range(round(1e6)), round(1e6))
    vals = list(zip(xs, ys))
    init = vals[0]
    rest = vals[1:]
    t = time()
    profile_tuple(init, rest)
    delta = time() - t
    print("profile_tuple: {}".format(delta))
    t = time()
    profile_point0(init, rest)
    delta = time() - t
    print("profile_point0: {}".format(delta))
    t = time()
    profile_point1(init, rest)
    delta = time() - t
    print("profile_point1: {}".format(delta))
    t = time()
    profile_point_dataclass0(init, rest)
    delta = time() - t
    print("profile_point_class0: {}".format(delta))
    t = time()
    profile_point_dataclass1(init, rest)
    delta = time() - t
    print("profile_point_class1: {}".format(delta))
    t = time()
    profile_point_dataclass2(init, rest)
    delta = time() - t
    print("profile_point_class2: {}".format(delta))


