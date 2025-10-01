from typing import override

import pygame as pg
from pygame.math import Vector2
from pygame.surface import Surface

from app.objects.base import ObjectBase, SpriteGroups
from app.utils import constants


class Missile(ObjectBase):
    def __init__(self, spawn_position: Vector2, rotation: float, groups: SpriteGroups) -> None:
        super().__init__(spawn_position, groups)
        self.radius: int = constants.MISSILE_RADIUS
        self.velocity: Vector2 = Vector2(0, 1).rotate(rotation)

    @override
    def draw(self, screen: Surface) -> None:
        color: str = 'green'
        width: int = 2
        self.rect = pg.draw.circle(screen, color, self.position, self.radius, width)

    @override
    def update(self, dt: float) -> None:
        self.position += self.velocity * constants.MISSILE_SPEED * dt
