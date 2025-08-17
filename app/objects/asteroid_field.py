import random
from typing import Any

import pygame as pg
from pygame.math import Vector2

from app.objects import Asteroid, AsteroidType
from app.utils import constants


class AsteroidField(pg.sprite.Sprite):
    spawn_points = [
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

    def __init__(self, collections: list[Any]) -> None:
        super().__init__()

        self.collections = collections
        self.spawn_timer: float = 0.0

    def spawn(self, position: Vector2, asteroid_type: AsteroidType, velocity: Vector2) -> None:
        asteroid = Asteroid(position, asteroid_type, self.collections)
        asteroid.velocity = velocity
        asteroid.add(*self.collections)

    def update(self, dt: float) -> None:
        self.spawn_timer += dt
        if self.spawn_timer > constants.ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0.0

            spawn_point: list[Any] = random.choice(self.spawn_points)
            velocity: Vector2 = spawn_point[0].rotate(random.randint(-30, 30))
            position: Vector2 = spawn_point[1](random.uniform(0, 1))
            asteroid_type = random.choice(list(AsteroidType))
            self.spawn(position, asteroid_type, velocity)
