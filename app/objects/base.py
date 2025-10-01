from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from pygame.math import Vector2
from pygame.sprite import AbstractGroup, Sprite
from pygame.surface import Surface

SpriteGroups = Sequence[AbstractGroup[Any]]


class ObjectBase(ABC, Sprite):
    def __init__(self, spawn_position: Vector2, groups: SpriteGroups) -> None:
        super().__init__(*groups)
        self._groups = groups
        self.position: Vector2 = Vector2(spawn_position)

    @abstractmethod
    def draw(self, screen: Surface) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass
