import random
from typing import Any, Self

import pygame as pg
from pygame.math import Vector2
from pygame.sprite import Sprite

from app.objects import Asteroid, AsteroidType
from app.objects.base import SpriteGroups
from app.utils import constants


class AsteroidField(Sprite):
    _instance: Self | None = None
    _initialized: bool = False
    _spawn_points = [
        # Left
        [
            pg.math.Vector2(1, 0),
            lambda y: pg.math.Vector2(-AsteroidType.LARGE.size, y * constants.SCREEN_HEIGHT),
        ],
        # Right
        [
            pg.math.Vector2(-1, 0),
            lambda y: pg.math.Vector2(constants.SCREEN_WIDTH + AsteroidType.LARGE.size, y * constants.SCREEN_HEIGHT),
        ],
        # Bottom - Y axis is inverted
        [
            pg.math.Vector2(0, -1),
            lambda x: pg.math.Vector2(x * constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT + AsteroidType.LARGE.size),
        ],
        # Top - Y axis is inverted
        [
            pg.math.Vector2(0, 1),
            lambda x: pg.math.Vector2(x * constants.SCREEN_WIDTH, -AsteroidType.LARGE.size),
        ],
    ]
    _spawn_timer: float = 0.0
    _asteroid_groups: SpriteGroups | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance  # type: ignore

    def __init__(self, groups: SpriteGroups, asteroid_groups: SpriteGroups) -> None:
        if not self._initialized:
            super().__init__(*groups)
            self._initialized = True
            self._asteroid_groups = asteroid_groups

    def spawn(self, position: Vector2, asteroid_type: AsteroidType, velocity: Vector2) -> None:
        assert self._asteroid_groups is not None
        asteroid = Asteroid(position, asteroid_type, self._asteroid_groups)
        asteroid.velocity = velocity

    def update(self, dt: float) -> None:
        self._spawn_timer += dt
        if self._spawn_timer > constants.ASTEROID_SPAWN_RATE:
            self._spawn_timer = 0.0

            spawn_point: list[Any] = random.choice(self._spawn_points)
            velocity: Vector2 = spawn_point[0].rotate(random.randint(-30, 30))
            position: Vector2 = spawn_point[1](random.uniform(0, 1))
            asteroid_type = random.choice(list(AsteroidType))
            self.spawn(position, asteroid_type, velocity)
