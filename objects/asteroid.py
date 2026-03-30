from __future__ import annotations

import logging
import random
from enum import Enum
from typing import TYPE_CHECKING, Any

import pygame as pg
from pygame.sprite import AbstractGroup

from core import (
    ASTEROID_LARGE_RADIUS,
    ASTEROID_LARGE_SCORE,
    ASTEROID_LARGE_SPEED,
    ASTEROID_MEDIUM_RADIUS,
    ASTEROID_MEDIUM_SCORE,
    ASTEROID_MEDIUM_SPEED,
    ASTEROID_SMALL_RADIUS,
    ASTEROID_SMALL_SCORE,
    ASTEROID_SMALL_SPEED,
    OBJECT_LINE_WIDTH,
)
from objects.base import BaseObject
from utils import entity_is_within_viewport, position_to_int_tuple

if TYPE_CHECKING:
    from scenes import GameScene

logger = logging.getLogger(__name__)


class AsteroidType(Enum):
    SMALL = (ASTEROID_SMALL_RADIUS, ASTEROID_SMALL_SPEED, ASTEROID_SMALL_SCORE)
    MEDIUM = (ASTEROID_MEDIUM_RADIUS, ASTEROID_MEDIUM_SPEED, ASTEROID_MEDIUM_SCORE)
    LARGE = (ASTEROID_LARGE_RADIUS, ASTEROID_LARGE_SPEED, ASTEROID_LARGE_SCORE)

    def __init__(self, size: int, speed: float, score: int) -> None:
        self.size: int = size
        self.speed: float = speed
        self.score: int = score


class Asteroid(BaseObject):
    def __init__(
        self,
        *groups: AbstractGroup[Any],
        scene: GameScene,
        position: tuple[int, int],
        rotation: float,
        asteroid_type: AsteroidType,
    ) -> None:
        super().__init__(
            *groups,
            scene=scene,
            position=pg.Vector2(position),
            rotation=rotation,
            radius=asteroid_type.size,
        )
        self.type = asteroid_type
        self.velocity = pg.Vector2(0, 1).rotate(rotation)

        logger.debug('Asteroid initialised at %s with type %s', position, asteroid_type.name)

    def draw(self, screen: pg.Surface) -> None:
        color = 'blue'
        pg.draw.circle(screen, color, self.rect.center, self.radius, OBJECT_LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * self.type.speed * dt
        self.rect.center = position_to_int_tuple(self.position)

        if not entity_is_within_viewport(self, self.scene.viewport):
            self.kill()
            logger.debug('Asteroid removed [out-of-bounds]')

    def split(self) -> None:
        if self.type == AsteroidType.SMALL:
            return
        match self.type:
            case AsteroidType.LARGE:
                new_type = AsteroidType.MEDIUM
            case AsteroidType.MEDIUM:
                new_type = AsteroidType.SMALL
        random_offset = random.uniform(20, 50)
        self._spawn_new_on_split(new_type, random_offset)
        self._spawn_new_on_split(new_type, -random_offset)

    def _spawn_new_on_split(self, asteroid_type: AsteroidType, offset: float) -> None:
        new_velocity = self.velocity.rotate(offset)
        new_rotation = pg.Vector2(0, 1).angle_to(new_velocity)
        asteroid_init_position = position_to_int_tuple(self.position)
        asteroid_groups = (self.scene.drawable, self.scene.updatable, self.scene.asteroids)
        Asteroid(
            *asteroid_groups,
            scene=self.scene,
            position=asteroid_init_position,
            rotation=new_rotation,
            asteroid_type=asteroid_type,
        )
