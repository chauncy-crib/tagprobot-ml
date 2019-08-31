from enum import Enum
import pygame
from typing import Tuple
import uuid

from visualization.drawable import Drawable


class Team(Enum):
    EGO = 0
    FRIEND = 1
    FOE = 2


class Ball(Drawable):
    def __init__(self, x: int, y: int, team: Team) -> None:
        self.id = uuid.uuid4()

        self.team = team
        self.color: Tuple[int, int, int] = (255, 255, 255)
        if self.team is Team.EGO:
            self.color = (255, 200, 0)
        elif self.team is Team.FRIEND:
            self.color = (255, 0, 0)
        elif self.team is Team.FOE:
            self.color = (0, 0, 255)
        else:
            raise ValueError("You must be self, friend, or foe!")

        self.radius = 19  # pixels

        self.x = x
        self.y = y

        self.vx = 0
        self.vy = 0

    def get_shape(self):
        return (pygame.draw.ellipse, self.color,
                pygame.Rect(self.x - self.radius,
                            self.y - self.radius,
                            2*self.radius,
                            2*self.radius))
