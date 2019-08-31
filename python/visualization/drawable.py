from abc import ABC, abstractmethod
import pygame

class Drawable(ABC):
    @abstractmethod
    def get_shape(self):
        pass

    def draw(self, screen):
        draw_func, color, shape = self.get_shape()
        draw_func(screen, color, shape)