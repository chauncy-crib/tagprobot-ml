import pygame
from dataclasses import dataclass
from visualization.shape import Shape

side_length = 20
color = (255, 255, 153)


@dataclass(frozen=True)
class Flag(Shape):
    x: int
    y: int

    def get_shape(self):
        return (pygame.draw.rect, color,
                pygame.Rect(self.x - 0.5*side_length,
                            self.y - 0.5*side_length,
                            side_length,
                            side_length))
