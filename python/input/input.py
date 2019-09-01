from typing import Dict
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Keys:
    left_pressed: bool
    right_pressed: bool
    up_pressed: bool
    down_pressed: bool


@dataclass(frozen=True)
class Input:
    keys: Dict[UUID, Keys]
