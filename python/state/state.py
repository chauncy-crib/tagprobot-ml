import pygame
from typing import List, Dict
import uuid

from .ball import Ball
from .flag import Flag


class State:
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
        ids: List[uuid.UUID] = list(map(lambda b: b.id, all_balls))
        assert(len(set(ids)) == len(ids))
        self.balls: Dict[uuid.UUID, Ball] = dict(zip(ids, all_balls))

        self.flag = flag

    def draw(self, screen):
        for ball_id, ball in self.balls.items():
            ball.draw(screen)

        self.flag.draw(screen)
