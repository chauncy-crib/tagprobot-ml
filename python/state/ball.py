from enum import Enum
import pygame
from uuid import UUID
from dataclasses import dataclass

from visualization.shape import Shape


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
    vx: int = 0
    vy: int = 0
    radius: int = 19

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
                pygame.Rect(self.x - self.radius,
                            self.y - self.radius,
                            2*self.radius,
                            2*self.radius))

    def move(self, dt: int) -> None:
        self.x += self.vx * dt / 1000
        self.y += self.vy * dt / 1000
