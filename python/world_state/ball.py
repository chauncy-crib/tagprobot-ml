import pygame
from typing import Tuple
import uuid

from visualization.drawable import Drawable


class Ball(Drawable):
    def __init__(self, x: int, y: int, color: Tuple[int]) -> None:
        self.id = uuid.uuid4()

        self.radius = 19  # pixels
        self.color = color

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
