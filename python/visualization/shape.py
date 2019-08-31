from abc import abstractmethod
from visualization.drawable import Drawable


class Shape(Drawable):
    @abstractmethod
    def get_shape(self):
        pass

    def draw(self, screen):
        draw_func, color, shape = self.get_shape()
        draw_func(screen, color, shape)
