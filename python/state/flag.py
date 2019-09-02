from dataclasses import dataclass
import pygame

from visualization.shape import Shape

side_length = 30
color = (255, 255, 153)


@dataclass
class Flag(Shape):
    x: float
    y: float
    radius: int = 15  # pixels

    being_carried: bool = False

    def get_shape(self):
        return (pygame.draw.rect, color,
                pygame.Rect(self.x - 0.5*side_length,
                            self.y - 0.5*side_length,
                            side_length,
                            side_length))
