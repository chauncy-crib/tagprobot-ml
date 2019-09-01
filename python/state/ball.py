from enum import Enum
import pygame
from uuid import UUID
from dataclasses import dataclass

from visualization.shape import Shape

radius: int = 19
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
    # velocities in pixels/second
    vx: float = 0
    vy: float = 0
    # acceleration in pixels/second^2
    ax: int = 0
    ay: int = 0

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

    def update(self, dt: int) -> None:
        """
        :param int dt: time elapsed in milliseconds
        """
        self.apply_drag(dt)
        self.move(dt)

    def apply_drag(self, dt: int) -> None:
        self.vx -= self.vx * damping_coefficient * dt / 1000
        self.vy -= self.vy * damping_coefficient * dt / 1000

    def move(self, dt: int) -> None:
        self.x += self.vx * dt / 1000
        self.y += self.vy * dt / 1000
