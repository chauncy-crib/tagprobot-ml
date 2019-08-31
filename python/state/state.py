from typing import List, Dict
import uuid

from visualization.drawable import Drawable
from input.input import Input
from .ball import Ball
from .flag import Flag


class State(Drawable):
    def __init__(
        self,
        enemy_balls: List[Ball],
        friendly_balls: List[Ball],
        ego_ball: Ball,
        flag: Flag
    ) -> None:
        assert(len(enemy_balls) <= 4)
        assert(len(friendly_balls) < 4)

        all_balls = enemy_balls + friendly_balls + [ego_ball]
        ids: List[uuid.UUID] = [b.id for b in all_balls]
        assert(len(set(ids)) == len(ids))
        self.balls: Dict[uuid.UUID, Ball] = dict(zip(ids, all_balls))

        self.flag = flag

    def draw(self, screen) -> None:
        for ball_id, ball in self.balls.items():
            ball.draw(screen)

        self.flag.draw(screen)

    # See python/README.md for explanation of these strange type hints
    def handle_inputs(self, input: Input) -> 'State':
        return self

    def next_state(self, dt: int) -> 'State':
        """
        :param int dt: time elapsed in milliseconds
        """
        return self
