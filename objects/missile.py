import logging
from typing import Any

import pygame as pg
from pygame.sprite import AbstractGroup

from core import MISSILE_RADIUS, MISSILE_SPEED
from objects.base import BaseObject
from scenes import GameScene
from utils import entity_is_within_viewport, position_to_int_tuple

logger = logging.getLogger(__name__)


class Missile(BaseObject):
    def __init__(
        self,
        *groups: AbstractGroup[Any],
        scene: GameScene,
        position: tuple[int, int],
        rotation: float,
    ) -> None:
        super().__init__(*groups, scene=scene, position=pg.Vector2(position), rotation=rotation)
        self.radius = MISSILE_RADIUS
        self.rect = pg.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.rect.center = position

        self.velocity = pg.Vector2(0, 1).rotate(self.rotation)
        self.color = 'green'
        self.line_width = 2

        logger.debug('Missile initialised at %s', position)

    def draw(self, screen: pg.Surface) -> None:
        pg.draw.circle(screen, self.color, self.rect.center, self.radius, self.line_width)

    def update(self, dt: float) -> None:
        self.position += self.velocity * MISSILE_SPEED * dt
        self.rect.center = position_to_int_tuple(self.position)

        if not entity_is_within_viewport(self, self.scene.viewport):
            self.kill()
            logger.debug('Missile removed [out-of-bounds]')
