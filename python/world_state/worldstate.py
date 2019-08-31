import pygame
from typing import List, Dict
import uuid

from .ball import Ball
from .flag import Flag


class WorldState:
    def __init__(
            self, enemy_balls: List[Ball],
            friendly_balls: List[Ball],
            ego_ball: Ball, flag: Flag, screen) -> None:
        assert(len(enemy_balls) <= 4)
        assert(len(friendly_balls) < 4)

        self.screen = screen

        self.blue_balls = enemy_balls
        self.red_balls = friendly_balls
        self.ego_ball = ego_ball

        all_balls = enemy_balls + friendly_balls + [ego_ball]
        print(all_balls)
        ids: List[uuid.UUID] = list(map(lambda b: b.id, all_balls))
        print(ids)
        assert(len(set(ids)) == len(ids))
        self.balls: Dict[uuid.UUID, Ball] = dict(zip(ids, all_balls))

        self.flag = flag

    def draw(self):
        for ball_id, ball in self.balls.items():
            ball.draw(self.screen)

        self.flag.draw(self.screen)
