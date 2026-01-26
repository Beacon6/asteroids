import logging
import random
from collections.abc import Callable

import pygame as pg
from pygame.math import Vector2
from pygame.sprite import Sprite

from app.objects.asteroid import Asteroid, AsteroidType
from app.objects.scenes import GameScene
from app.settings import get_settings

logger = logging.getLogger(__name__)

SpawnPoints = list[tuple[Vector2, Callable[[float], Vector2]]]


class AsteroidField(Sprite):
    _settings = get_settings()

    def __init__(self, scene: GameScene) -> None:
        super().__init__()

        self.scene = scene

        screen_width = self._settings.screen_width
        screen_height = self._settings.screen_height
        self.spawn_points: SpawnPoints = [
            # Left
            (
                pg.math.Vector2(1, 0),
                lambda y: pg.math.Vector2(-AsteroidType.LARGE.size, y * screen_height),
            ),
            # Right
            (
                pg.math.Vector2(-1, 0),
                lambda y: pg.math.Vector2(screen_width + AsteroidType.LARGE.size, y * screen_height),
            ),
            # Bottom - Y axis is inverted
            (
                pg.math.Vector2(0, -1),
                lambda x: pg.math.Vector2(x * screen_width, screen_height + AsteroidType.LARGE.size),
            ),
            # Top - Y axis is inverted
            (
                pg.math.Vector2(0, 1),
                lambda x: pg.math.Vector2(x * screen_width, -AsteroidType.LARGE.size),
            ),
        ]

        self.scene.updatable.add(self)

        self.spawn_timer = self._settings.asteroid_spawn_rate
        logger.debug('Asteroid field initialised')

    def update(self, dt: float) -> None:
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            spawn_point = random.choice(self.spawn_points)
            velocity = spawn_point[0].rotate(random.randint(-30, 30))
            position = spawn_point[1](random.uniform(0, 1))
            asteroid_type = random.choice(list(AsteroidType))
            self.spawn(position, asteroid_type, velocity)

    def spawn(self, position: Vector2, asteroid_type: AsteroidType, velocity: Vector2) -> None:
        asteroid = Asteroid(self.scene, position, asteroid_type)
        asteroid.velocity = velocity
        self.spawn_timer = self._settings.asteroid_spawn_rate
