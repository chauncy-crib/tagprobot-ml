import pygame
from typing import List

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

        self.balls = {}
        for blue_ball in self.blue_balls:
            if blue_ball.id in self.balls:
                raise ValueError(
                    "Ball id {} already exists".format(blue_ball.id))
            self.balls[blue_ball.id] = blue_ball
        for red_ball in self.red_balls:
            if red_ball.id in self.balls:
                raise ValueError(
                    "Ball id {} already exists".format(blue_ball.id))
            self.balls[red_ball.id] = red_ball
        if ego_ball.id in self.balls:
            raise ValueError("Ball id {} already exists".format(blue_ball.id))
        self.balls[ego_ball.id] = ego_ball

        self.flag = flag

    def draw(self):
        for ball_id, ball in self.balls.items():
            ball.draw(self.screen)

        self.flag.draw(self.screen)
