import logging

import pygame as pg
from pygame.math import Vector2
from pygame.sprite import Sprite

from app.objects.scenes import GameScene
from app.settings import get_settings

logger = logging.getLogger(__name__)


class Missile(Sprite):
    _settings = get_settings()

    def __init__(self, scene: GameScene, position: Vector2, rotation: float) -> None:
        super().__init__()

        self.scene = scene

        self.position = Vector2(position)
        self.rotation = rotation

        self.scene.drawable.add(self)
        self.scene.updatable.add(self)
        self.scene.projectiles.add(self)

        self.velocity = Vector2(0, 1).rotate(rotation)
        logger.debug(f'Missile initialised at {self.position}')

    def draw(self) -> None:
        self.rect = pg.draw.circle(
            self.scene.screen,
            self._settings.missile_color,
            self.position,
            self._settings.missile_radius,
            self._settings.missile_line_width,
        )

    def update(self, dt: float) -> None:
        self.position += self.velocity * self._settings.missile_speed * dt
