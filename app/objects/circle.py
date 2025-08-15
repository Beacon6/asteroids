from abc import abstractmethod

import pygame as pg
from pygame.math import Vector2
from pygame.surface import Surface


class CircleBase(pg.sprite.Sprite):
    def __init__(self, x: float, y: float, radius: int) -> None:
        super().__init__()

        self.position: Vector2 = pg.math.Vector2(x, y)
        self.radius: int = radius
        self.rect = pg.Rect(self.position, (self.radius * 2, self.radius * 2))

    @abstractmethod
    def draw(self, screen: Surface) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass
