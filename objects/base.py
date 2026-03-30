from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, override

import pygame as pg
from pygame.sprite import AbstractGroup, Sprite

from core import get_settings

if TYPE_CHECKING:
    from scenes import GameScene


class SpriteWrapper(Sprite, ABC):
    @override
    def __init__(self, *groups: AbstractGroup[Any]) -> None:
        super().__init__(*groups)
        self.rect = pg.Rect(0, 0, 0, 0)
        self.image = pg.Surface((0, 0))

    @abstractmethod
    def draw(self, screen: pg.Surface) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass


class BaseObject(SpriteWrapper, ABC):
    @override
    def __init__(
        self,
        *groups: AbstractGroup[Any],
        scene: GameScene,
        position: pg.Vector2,
        rotation: float,
    ) -> None:
        super().__init__(*groups)
        self._settings = get_settings()
        self.scene = scene
        self.position = position
        self.rotation = rotation
