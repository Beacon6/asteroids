from abc import ABC, abstractmethod
from typing import override

import pygame as pg
from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.surface import Surface

from app.utils import constants


class MissileBase(ABC, Sprite):
    def __init__(self, spawn_position: Vector2, rotation: float) -> None:
        super().__init__()
        self.radius: int = constants.MISSILE_RADIUS
        self.position: Vector2 = Vector2(spawn_position)
        self.velocity: Vector2 = Vector2(0, 1).rotate(rotation)

    @abstractmethod
    def draw(self, screen: Surface) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass


class Missile(MissileBase):
    @override
    def draw(self, screen: Surface) -> None:
        color: str = 'green'
        width: int = 2
        self.rect = pg.draw.circle(screen, color, self.position, self.radius, width)

    @override
    def update(self, dt: float) -> None:
        self.position += self.velocity * constants.MISSILE_SPEED * dt
