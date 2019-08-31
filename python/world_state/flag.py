import pygame
from visualization.drawable import Drawable

class Flag(Drawable):
    def __init__(self, x: int, y: int) -> None:
        self.side_length = 20

        self.x = x
        self.y = y

        self.color = (255,255,153)

    def get_shape(self):
        return (pygame.draw.rect, self.color, pygame.Rect(self.x - 0.5*self.side_length, self.y - 0.5*self.side_length, self.side_length, self.side_length))