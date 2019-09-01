import copy
from dataclasses import dataclass
from enum import Enum
import pygame
from typing import Tuple
from uuid import UUID

from utils.math import clamp
from input.input import Keys
from visualization.shape import Shape

radius: int = 19  # pixels
max_speed: float = 250  # pixels / second
default_accel: int = 150  # pixels / second^2
damping_coefficient: float = 0.5


class Team(Enum):
    EGO = 0
    FRIEND = 1
    FOE = 2


@dataclass
class Ball(Shape):
    # floats needed in order to store position at fractional pixels
    x: float
    y: float
    id: UUID
    team: Team
    # velocities in pixels / second
    vx: float = 0
    vy: float = 0
    # acceleration in pixels / second^2
    ax: int = 0
    ay: int = 0

    has_flag: bool = False

    has_jj: bool = False
    has_rb: bool = False
    has_tp: bool = False

    on_team_tile: bool = False

    radius: int = radius

    def get_shape(self):
        if self.team is Team.EGO:
            color = (255, 200, 0)
        elif self.team is Team.FRIEND:
            color = (255, 0, 0)
        elif self.team is Team.FOE:
            color = (0, 0, 255)
        else:
            raise ValueError("You must be self, friend, or foe!")
        return (pygame.draw.ellipse,
                color,
                pygame.Rect(self.x - radius,
                            self.y - radius,
                            2*radius,
                            2*radius))

    def is_on_team_tile(self, map) -> bool:
        # TODO (altodyte): This should return True if the ball is on a team tile matching its color
        return False

    def handle_input(self, keypresses: Keys) -> None:
        self.ax, self.ay = self.accels_from_input(keypresses)

    def simulate_input(self, keypresses: Keys) -> 'Ball':
        future_ball = copy.deepcopy(self)
        self.ax, self.ay = self.accels_from_input(keypresses)
        return future_ball

    def accels_from_input(self, keypresses: Keys) -> Tuple[int, int]:
        ax = self._accel_from_input(keypresses.left_pressed, keypresses.right_pressed)
        ay = self._accel_from_input(keypresses.up_pressed, keypresses.down_pressed)
        return (ax, ay)

    def _accel_from_input(self, negative_dir_pressed: bool, positive_dir_pressed: bool) -> int:
        if positive_dir_pressed == negative_dir_pressed:
            return 0
        accel: float = -default_accel if negative_dir_pressed else default_accel
        use_team_tiles = (not self.has_flag) and self.is_on_team_tile(None)
        if self.has_jj and not use_team_tiles:
            accel *= 1.25  # bonus for just having juke juice
        elif self.has_jj:
            accel *= 1.75  # bonus for having juke juice and team tile
        elif use_team_tiles:
            accel *= 1.50  # bonus for just having team tile
        return int(accel)

    def update(self, dt: int) -> None:
        self.on_team_tile = self.is_on_team_tile(None)
        self.x, self.y, self.vx, self.vy = self.simulate_update(dt)

    def simulate_update(self, dt: int) -> Tuple[float, float, float, float]:
        """
        :param int dt: time elapsed in milliseconds
        See https://www.reddit.com/r/TagPro/wiki/physics for details on physics rules.
        """
        max_vel = max_speed if not self.on_team_tile else max_speed * 2.0
        vx = self.vx + clamp((self.ax - self.vx * damping_coefficient)
                             * dt * 0.001, -max_vel, max_vel)
        vy = self.vy + clamp((self.ay - self.vy * damping_coefficient)
                             * dt * 0.001, -max_vel, max_vel)

        x = self.x + vx * dt * 0.001
        y = self.y + vy * dt * 0.001

        return (x, y, vx, vy)
