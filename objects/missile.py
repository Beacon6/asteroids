from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import pygame as pg
from pygame.sprite import AbstractGroup

from core import MISSILE_RADIUS, MISSILE_SPEED, OBJECT_LINE_WIDTH
from objects.base import BaseObject
from utils import entity_is_within_viewport, position_to_int_tuple

if TYPE_CHECKING:
    from scenes import GameScene

logger = logging.getLogger(__name__)


class Missile(BaseObject):
    def __init__(
        self,
        *groups: AbstractGroup[Any],
        scene: GameScene,
        position: tuple[int, int],
        rotation: float,
    ) -> None:
        super().__init__(
            *groups,
            scene=scene,
            position=pg.Vector2(position),
            rotation=rotation,
            radius=MISSILE_RADIUS,
        )
        self.velocity = pg.Vector2(0, 1).rotate(self.rotation)

        logger.debug('Missile initialised at %s', position)

    def draw(self, screen: pg.Surface) -> None:
        color = 'green'
        pg.draw.circle(screen, color, self.rect.center, self.radius, OBJECT_LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * MISSILE_SPEED * dt
        self.rect.center = position_to_int_tuple(self.position)

        if not entity_is_within_viewport(self, self.scene.viewport):
            self.kill()
            logger.debug('Missile removed [out-of-bounds]')
