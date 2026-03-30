from __future__ import annotations

import logging
import random
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, override

import pygame as pg
from pygame.sprite import AbstractGroup

from core import ASTEROID_LARGE_RADIUS, ASTEROID_SPAWN_RATE
from objects.asteroid import Asteroid, AsteroidType
from objects.base import SpriteWrapper
from utils import position_to_int_tuple

if TYPE_CHECKING:
    from scenes import GameScene

logger = logging.getLogger(__name__)

SpawnPoints = list[tuple[pg.Vector2, Callable[[float], pg.Vector2]]]


class AsteroidField(SpriteWrapper):
    def __init__(self, *groups: AbstractGroup[Any], scene: GameScene) -> None:
        super().__init__(*groups)
        self.scene = scene

        self.spawn_points: SpawnPoints = self._get_spawn_points()
        self.spawn_timer = ASTEROID_SPAWN_RATE

        logger.debug('Asteroid field initialised')

    @override
    def draw(self, screen: pg.Surface) -> None:
        pass

    @override
    def update(self, dt: float) -> None:
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            direction, position_fn = random.choice(self.spawn_points)
            asteroid_type = random.choice(list(AsteroidType))
            position = position_to_int_tuple(position_fn(random.uniform(0, 1)))
            velocity = direction.rotate(random.randint(-30, 30))
            self._spawn(asteroid_type, position, velocity)

    def _get_spawn_points(self) -> SpawnPoints:
        screen_width = self.scene.viewport.width
        screen_height = self.scene.viewport.height
        return [
            # Left
            (
                pg.Vector2(1, 0),
                lambda y: pg.Vector2(-ASTEROID_LARGE_RADIUS, y * screen_height),
            ),
            # Right
            (
                pg.Vector2(-1, 0),
                lambda y: pg.Vector2(screen_width + ASTEROID_LARGE_RADIUS, y * screen_height),
            ),
            # Bottom - Y axis is inverted
            (
                pg.Vector2(0, -1),
                lambda x: pg.Vector2(x * screen_width, screen_height + ASTEROID_LARGE_RADIUS),
            ),
            # Top - Y axis is inverted
            (
                pg.Vector2(0, 1),
                lambda x: pg.Vector2(x * screen_width, -ASTEROID_LARGE_RADIUS),
            ),
        ]

    def _spawn(
        self,
        asteroid_type: AsteroidType,
        position: tuple[int, int],
        velocity: pg.Vector2,
    ) -> None:
        asteroid_groups = (self.scene.drawable, self.scene.updatable, self.scene.asteroids)
        rotation = pg.Vector2(0, 1).angle_to(velocity)
        Asteroid(
            *asteroid_groups,
            scene=self.scene,
            position=position,
            rotation=rotation,
            asteroid_type=asteroid_type,
        )
        self.spawn_timer = ASTEROID_SPAWN_RATE
