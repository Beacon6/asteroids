import random
from typing import Any

import pygame
from pygame.math import Vector2

from app.objects.asteroid import Asteroid
from app.settings import constants


class AsteroidField(pygame.sprite.Sprite):
    spawn_points = [
        # Left
        [
            pygame.math.Vector2(1, 0),
            lambda y: pygame.math.Vector2(-constants.ASTEROID_MAX_RADIUS, y * constants.SCREEN_HEIGHT),
        ],
        # Right
        [
            pygame.math.Vector2(-1, 0),
            lambda y: pygame.math.Vector2(
                constants.SCREEN_WIDTH + constants.ASTEROID_MAX_RADIUS, y * constants.SCREEN_HEIGHT
            ),
        ],
        # Bottom - Y axis is inverted
        [
            pygame.math.Vector2(0, -1),
            lambda x: pygame.math.Vector2(
                x * constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT + constants.ASTEROID_MAX_RADIUS
            ),
        ],
        # Top - Y axis is inverted
        [
            pygame.math.Vector2(0, 1),
            lambda x: pygame.math.Vector2(x * constants.SCREEN_WIDTH, -constants.ASTEROID_MAX_RADIUS),
        ],
    ]

    def __init__(self, collections: list[Any]) -> None:
        super().__init__()

        self.collections = collections
        self.spawn_timer: float = 0.0

    def spawn(self, position: Vector2, radius: int, velocity: Vector2) -> None:
        asteroid = Asteroid(position.x, position.y, radius, self.collections)
        asteroid.velocity = velocity
        asteroid.add(*self.collections)

    def update(self, dt: float) -> None:
        self.spawn_timer += dt
        if self.spawn_timer > constants.ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0.0

            spawn_point: list[Any] = random.choice(self.spawn_points)
            velocity: Vector2 = spawn_point[0].rotate(random.randint(-30, 30))
            position: Vector2 = spawn_point[1](random.uniform(0, 1))
            asteroid_kind = random.randint(1, constants.ASTEROID_KINDS)
            self.spawn(position, asteroid_kind * constants.ASTEROID_MIN_RADIUS, velocity)
