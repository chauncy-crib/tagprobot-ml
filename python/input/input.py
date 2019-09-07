from dataclasses import dataclass
import pygame
import random
from uuid import UUID
from typing import Dict


@dataclass
class Keys:
    left_pressed: bool = False
    right_pressed: bool = False
    up_pressed: bool = False
    down_pressed: bool = False

    @staticmethod
    def from_pygame_pressed(pyg_keys) -> 'Keys':
        return Keys(pyg_keys[pygame.K_LEFT], pyg_keys[pygame.K_RIGHT],
                    pyg_keys[pygame.K_UP], pyg_keys[pygame.K_DOWN])

    @staticmethod
    def random_keys() -> 'Keys':
        press_left = bool(random.getrandbits(1))
        press_up = bool(random.getrandbits(1))
        return Keys(press_left, not press_left, press_up, not press_up)


@dataclass
class Input:
    commands: Dict[UUID, Keys]
