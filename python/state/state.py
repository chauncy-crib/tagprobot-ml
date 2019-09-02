import random
from typing import Dict, List
from uuid import UUID

from visualization.drawable import Drawable
from input.input import Input
from utils import math

from state.ball import Ball, Team
from state.flag import Flag


class State(Drawable):
    def __init__(self, balls: List[Ball], flag: Flag):
        self.flag = flag
        self.balls: Dict[UUID, Ball] = {b.id: b for b in balls}
        self.friendly_score = 0
        self.enemy_score = 0

        num_foe_balls = sum(1 for b in balls if b.team is Team.FOE)
        num_friendly_balls = sum(1 for b in balls if b.team is Team.FRIEND)
        num_ego_balls = sum(1 for b in balls if b.team is Team.EGO)
        assert(num_foe_balls <= 4)
        assert(num_friendly_balls < 4)
        assert(num_ego_balls == 1)
        assert(len(self.balls) == len(balls))

    def draw(self, screen) -> None:
        for ball in self.balls.values():
            ball.draw(screen)

        self.flag.draw(screen)

    def handle_input(self, user_input: Input) -> None:
        for uid, keys in user_input.commands.items():
            self.balls[uid].handle_input(keys)

    def next_state(self, dt: int) -> None:
        """
        :param int dt: time elapsed in milliseconds
        """
        for b in self.balls.values():
            b.update(dt)
            if b.has_flag:
                self.flag.x, self.flag.y = b.x, b.y

        # TODO check if any balls have popped on the environment (e.g. spikes).

        # Check if any balls have tagged another ball. Do in random order for fairness.
        for ball in random.sample(list(self.balls.values()), len(self.balls)):
            if self.ball_gets_tagged(ball):
                if ball.has_flag:
                    self.flag.being_carried = False
                ball.handle_pop()

        # TODO decide if the flag should be automatically passed to a tagger.
        # If the flag isn't being carried, see if any balls can grab it. Random order for fairness.
        if not self.flag.being_carried:
            for ball in random.sample(list(self.balls.values()), len(self.balls)):
                if self.ball_gets_flag(ball):
                    self.flag.being_carried = True
                    ball.has_flag = True
                    break

    def get_ego_ball(self):
        return next(ball for ball in self.balls.values() if ball.team == Team.EGO)

    def ball_gets_flag(self, ball: Ball) -> bool:
        if self.flag.being_carried:
            return False
        combined_radius = ball.radius + self.flag.radius
        ball_flag_dist = math.dist(ball.x, ball.y, self.flag.x, self.flag.y)

        return ball_flag_dist <= combined_radius

    def ball_gets_tagged(self, ball: Ball) -> bool:
        for other_ball in self.balls.values():
            if other_ball.id == ball.id:
                continue
            if other_ball.is_popped or ball.is_popped:
                continue
            combined_radius = ball.radius + other_ball.radius
            ball_ball_dist = math.dist(ball.x, ball.y, other_ball.x, other_ball.y)

            if other_ball.has_tp or (ball.has_flag and not ball.on_same_team(other_ball)):
                if ball_ball_dist <= combined_radius:
                    return True
        return False
