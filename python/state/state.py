from typing import List
import uuid
from dataclasses import dataclass

from visualization.drawable import Drawable
from input.input import Input
from .ball import Ball
from .flag import Flag


@dataclass(frozen=True)
class State(Drawable):
    enemy_balls: List[Ball]
    friendly_balls: List[Ball]
    ego_ball: Ball
    flag: Flag

    def __post_init__(self):
        assert(len(self.enemy_balls) <= 4)
        assert(len(self.friendly_balls) < 4)
        all_balls = self.all_balls()
        ids: List[uuid.UUID] = [b.id for b in all_balls]
        assert(len(set(ids)) == len(ids))

    def all_balls(self):
        return self.enemy_balls + self.friendly_balls + [self.ego_ball]

    def draw(self, screen) -> None:
        for ball in self.all_balls():
            ball.draw(screen)

        self.flag.draw(screen)

    def handle_inputs(self, input: Input) -> 'State':
        # TODO: implement this correctly in a subsequent PR
        return self

    def next_state(self, dt: int) -> 'State':
        """
        :param int dt: time elapsed in milliseconds
        """
        return State(
            enemy_balls=[b.move(dt) for b in self.enemy_balls],
            friendly_balls=[b.move(dt) for b in self.friendly_balls],
            ego_ball=self.ego_ball.move(dt),
            flag=self.flag
        )
