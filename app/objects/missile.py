import logging
from typing import override

import pygame as pg
from pygame.math import Vector2

from app.objects.base import CircleBase
from app.objects.scenes import GameScene

logger = logging.getLogger(__name__)


class Missile(CircleBase):
    def __init__(self, scene: GameScene, position: Vector2, rotation: float) -> None:
        super().__init__(scene, position, self._settings.missile_radius)

        self.rotation = rotation

        self.scene.projectiles.add(self)

        self.velocity = Vector2(0, 1).rotate(rotation)
        logger.debug(f'Missile initialised at {self.position}')

    @override
    def draw(self) -> None:
        self.rect = pg.draw.circle(
            self.scene.screen,
            self._settings.missile_color,
            self.position,
            self.radius,
            self._settings.missile_line_width,
        )

    @override
    def update(self, dt: float) -> None:
        self.position += self.velocity * self._settings.missile_speed * dt
