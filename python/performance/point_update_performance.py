import random
from utils.timeit import timeit
from copy import deepcopy
from typing import List, Tuple
from dataclasses import dataclass, replace
import sys
from os import pardir
from os.path import dirname, join
# we need to add the parent directory to the sys.path in order to import from
# other modules
sys.path.append(join(dirname(__file__), pardir))


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
6. Use a dataclass, and mutate the instance for each update
7. Use a dataclass, and deepcopy the instance, and then mutate it for each
   update


The performance of each of these options (in seconds, so large numbers are
bad):

1. profile_tuple: 0.14
2. profile_point0: 0.18
3. profile_point1: 0.35
4. profile_point_dataclass0: 1.08
5. profile_point_dataclass1: 0.36
6. profile_point_dataclass2: 0.18
7. profile_point_deepcopy: 6.36

Given the cleaner syntax of dataclasses, and equivalent performance, we
recommend using dataclasses wherever possible. Whenever possible, construct
new instances rather than mutating in place, in order to avoid deepcopy()ing
later.
"""


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


@dataclass
class DataPoint:
    x: int
    y: int


def profile_tuple(initial: Tuple[int, int], values: List[Tuple[int, int]]):
    tup = initial
    for (x0, y0) in values:
        tup = (x0, y0)  # noqa: F841


def profile_point0(initial: Tuple[int, int], values: List[Tuple[int, int]]):
    point = Point(initial[0], initial[1])
    for (x0, y0) in values:
        point.x = x0
        point.y = y0


def profile_point1(initial: Tuple[int, int], values: List[Tuple[int, int]]):
    point = Point(initial[0], initial[1])
    for (x0, y0) in values:
        point = Point(x0, y0)  # noqa: F841


def profile_point_dataclass0(initial: Tuple[int, int], values: List[Tuple[int, int]]):
    point = DataPoint(initial[0], initial[1])
    for (x0, y0) in values:
        point = replace(point, x=x0, y=y0)  # noqa: F841


def profile_point_dataclass1(initial: Tuple[int, int], values: List[Tuple[int, int]]):
    point = DataPoint(initial[0], initial[1])
    for (x0, y0) in values:
        point = DataPoint(x0, y0)  # noqa: F841


def profile_point_dataclass2(initial: Tuple[int, int], values: List[Tuple[int, int]]):
    point = DataPoint(initial[0], initial[1])
    for (x0, y0) in values:
        point.x = x0
        point.y = y0


def profile_point_deepcopy(initial: Tuple[int, int], values: List[Tuple[int, int]]):
    point = DataPoint(initial[0], initial[1])
    for (x0, y0) in values:
        copy = deepcopy(point)
        copy.x = x0
        copy.y = y0
        point = copy


if __name__ == "__main__":
    xs = random.sample(range(round(1e6)), round(1e6))
    ys = random.sample(range(round(1e6)), round(1e6))
    vals = list(zip(xs, ys))
    init = vals[0]
    rest = vals[1:]
    timeit(profile_tuple, init, rest)
    timeit(profile_point0, init, rest)
    timeit(profile_point1, init, rest)
    timeit(profile_point_dataclass0, init, rest)
    timeit(profile_point_dataclass1, init, rest)
    timeit(profile_point_dataclass2, init, rest)
    timeit(profile_point_deepcopy, init, rest)
