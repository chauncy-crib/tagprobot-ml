from typing import Dict, List
from uuid import UUID
from dataclasses import dataclass

from visualization.drawable import Drawable
from input.input import Input
from .ball import Ball, Team
from .flag import Flag


@dataclass
class State(Drawable):
    def __init__(self, balls: List[Ball], flag: Flag):
        self.flag = flag
        self.balls: Dict[UUID, Ball] = {b.id: b for b in balls}
        num_foe_balls = sum(1 for b in balls if b.team is Team.FOE)
        num_friendly_balls = sum(1 for b in balls if b.team is Team.FRIEND)
        assert(num_foe_balls <= 4)
        assert(num_friendly_balls < 4)
        assert(len(self.balls) == len(balls))

    def draw(self, screen) -> None:
        for ball in self.balls.values():
            ball.draw(screen)

        self.flag.draw(screen)

    def handle_inputs(self, input: Input) -> None:
        # TODO: implement this correctly in a subsequent PR
        pass

    def next_state(self, dt: int) -> None:
        """
        :param int dt: time elapsed in milliseconds
        """
        for b in self.balls.values():
            b.update(dt)
