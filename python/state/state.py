from typing import List, Dict
from dataclasses import dataclass, replace
from uuid import UUID

from visualization.drawable import Drawable
from input.input import Input, Keys
from utils import math

from state.ball import Ball, Team
from state.flag import Flag


@dataclass(frozen=True)
class State(Drawable):
    balls: List[Ball]
    flag: Flag
    friendly_score = 0
    enemy_score = 0

    def __post_init__(self):
        ball_ids = {b.id for b in self.balls}
        num_foe_balls = sum(1 for b in self.balls if b.team is Team.FOE)
        num_friendly_balls = sum(1 for b in self.balls if b.team is Team.FRIEND)
        num_ego_balls = sum(1 for b in self.balls if b.team is Team.EGO)
        assert(len(ball_ids) == len(self.balls))
        assert(num_foe_balls <= 4)
        assert(num_friendly_balls < 4)
        assert(num_ego_balls == 1)

    def draw(self, screen) -> None:
        for ball in self.balls:
            ball.draw(screen)
        self.flag.draw(screen)

    def _handle_input(self, user_input: Input) -> 'State':
        def pass_input_to_ball(ball: Ball, commands: Dict[UUID, Keys]):
            if ball.id not in commands:
                return ball
            return ball.handle_input(commands[ball.id])
        balls = [pass_input_to_ball(b, user_input.commands) for b in self.balls]
        return State(
            balls=balls,
            flag=self.flag
        )

    def _step_time(self, dt: int) -> 'State':
        balls = [b.update(dt) for b in self.balls]
        flag = self.flag
        for b in balls:
            if b.has_flag:
                flag = Flag(
                    x=b.x,
                    y=b.y,
                    being_carried=self.flag.being_carried
                )

        # TODO check if any balls have popped on the environment (e.g. spikes).

        # Check if any balls have tagged another ball. Do in random order for fairness.
        for i in range(len(balls)):
            ball = balls[i]
            if self.ball_gets_tagged(ball, balls):
                if ball.has_flag:
                    flag = Flag(flag.x, flag.y, being_carried=False)
                balls[i] = ball.handle_pop()

        # TODO decide if the flag should be automatically passed to a tagger.
        # If the flag isn't being carried, see if any balls can grab it. Random order for fairness.
        if not flag.being_carried:
            for i in range(len(balls)):
                ball = balls[i]
                if self.ball_gets_flag(ball, flag):
                    flag = Flag(flag.x, flag.y, being_carried=True)
                    balls[i] = replace(ball, has_flag=True)
                    break

        num_flag_carriers = sum(1 for b in balls if b.has_flag)
        assert(num_flag_carriers <= 1)
        return State(
            balls=balls,
            flag=flag,
        )

    def next_state(self, user_input: Input, dt: int) -> 'State':
        """
        :param user_input Input: key presses for each Ball
        :param int dt: time elapsed in milliseconds
        """
        inputs_applied: 'State' = self._handle_input(user_input)
        after_time_step: 'State' = inputs_applied._step_time(dt)
        return after_time_step

    def get_ego_ball(self):
        return next(ball for ball in self.balls.values() if ball.team == Team.EGO)

    @staticmethod
    def ball_gets_flag(ball: Ball, flag: Flag) -> bool:
        if flag.being_carried:
            return False
        combined_radius = ball.radius + flag.radius
        ball_flag_dist = math.dist(ball.x, ball.y, flag.x, flag.y)

        return ball_flag_dist <= combined_radius

    @staticmethod
    def ball_gets_tagged(ball: Ball, balls: List[Ball]) -> bool:
        for other_ball in balls:
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
