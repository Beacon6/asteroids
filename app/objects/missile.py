from typing import override

import pygame as pg
from pygame.math import Vector2
from pygame.surface import Surface

from app.objects.circle import CircleBase
from app.utils import constants


class Missile(CircleBase):
    def __init__(self, x: float, y: float, radius: int, rotation: float):
        super().__init__(x, y, radius)

        self.velocity: Vector2 = pg.math.Vector2(0, 1).rotate(rotation)

    @override
    def draw(self, screen: Surface) -> None:
        color: str = 'green'
        center: Vector2 = self.position
        radius: int = self.radius
        width: int = 2

        self.rect = pg.draw.circle(screen, color, center, radius, width)

    @override
    def update(self, dt: float) -> None:
        self.move(dt)

    def move(self, dt: float) -> None:
        self.position += self.velocity * constants.MISSILE_SPEED * dt
