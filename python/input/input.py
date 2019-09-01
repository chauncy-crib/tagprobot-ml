from typing import Dict
from dataclasses import dataclass
from uuid import UUID

import pygame


@dataclass(frozen=True)
class Keys:
    left_pressed: bool
    right_pressed: bool
    up_pressed: bool
    down_pressed: bool

    @staticmethod
    def from_pygame_pressed(pyg_keys) -> 'Keys':
        return Keys(pyg_keys[pygame.K_LEFT], pyg_keys[pygame.K_RIGHT],
                    pyg_keys[pygame.K_UP], pyg_keys[pygame.K_DOWN])


@dataclass(frozen=True)
class Input:
    commands: Dict[UUID, Keys]
