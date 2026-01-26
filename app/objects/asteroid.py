import logging
from enum import Enum

import pygame as pg
from pygame.math import Vector2
from pygame.sprite import Sprite

from app.objects.scenes import GameScene
from app.settings import get_settings

logger = logging.getLogger(__name__)


class AsteroidType(Enum):
    SMALL = (20, 0.1, 100)  # size, speed, score
    MEDIUM = (40, 0.05, 50)
    LARGE = (60, 0.02, 20)

    def __init__(self, size: int, speed: float, score: int) -> None:
        self.size: int = size
        self.speed: float = speed
        self.score: int = score


class Asteroid(Sprite):
    _settings = get_settings()

    def __init__(self, scene: GameScene, position: Vector2, asteroid_type: AsteroidType) -> None:
        super().__init__()

        self.scene = scene

        self.position = Vector2(position)
        self.type = asteroid_type

        self.scene.drawable.add(self)
        self.scene.updatable.add(self)
        self.scene.asteroids.add(self)

        self.velocity: Vector2 = Vector2(0, 1)
        logger.debug(f'Asteroid initialised at {self.position}')

    def draw(self) -> None:
        self.rect = pg.draw.circle(
            self.scene.screen,
            self._settings.asteroid_color,
            self.position,
            self.type.size,
            self._settings.asteroid_line_width,
        )

    def update(self, dt: float) -> None:
        self.position += self.velocity * self.type.speed * dt

    # def split(self) -> None:
    #     if self.type == AsteroidType.SMALL:
    #         return
    #
    #     match self.type:
    #         case AsteroidType.LARGE:
    #             new_type = AsteroidType.MEDIUM
    #         case AsteroidType.MEDIUM:
    #             new_type = AsteroidType.SMALL
    #     assert isinstance(new_type, AsteroidType)
    #
    #     random_offset = random.uniform(20, 50)
    #     self._spawn_new_on_split(new_type, random_offset)
    #     self._spawn_new_on_split(new_type, -random_offset)
    #
    # def _spawn_new_on_split(self, asteroid_type: AsteroidType, random_offset: float) -> None:
    #     new_asteroid = Asteroid(
    #         self.position,
    #         asteroid_type,
    #         self._groups,
    #     )
    #     new_asteroid.velocity = self.velocity.rotate(random_offset)
