import logging
import random
from enum import Enum
from typing import override

import pygame as pg
from pygame.math import Vector2

from app.objects.base import CircleBase
from app.objects.scenes import GameScene

logger = logging.getLogger(__name__)


class AsteroidType(Enum):
    SMALL = (20, 0.1, 100)  # size, speed, score
    MEDIUM = (40, 0.05, 50)
    LARGE = (60, 0.02, 20)

    def __init__(self, size: int, speed: float, score: int) -> None:
        self.size: int = size
        self.speed: float = speed
        self.score: int = score


class Asteroid(CircleBase):
    def __init__(self, scene: GameScene, position: Vector2, asteroid_type: AsteroidType) -> None:
        super().__init__(scene, position, asteroid_type.size)

        self.type = asteroid_type

        self.scene.asteroids.add(self)

        self.rect = pg.Rect(0, 0, self.type.size * 2, self.type.size * 2)
        self.rect.center = (int(position.x), int(position.y))
        self.velocity: Vector2 = Vector2(0, 1)
        logger.debug(f'Asteroid initialised at {self.position}')

    @override
    def draw(self) -> None:
        pg.draw.circle(
            self.scene.screen,
            self._settings.asteroid_color,
            self.rect.center,
            self.radius,
            self._settings.asteroid_line_width,
        )

    @override
    def update(self, dt: float) -> None:
        self.position += self.velocity * self.type.speed * dt
        self.rect.center = (int(self.position.x), int(self.position.y))

        if not self._is_on_screen():
            logger.debug('Asteroid removed')
            self.kill()

    def split(self) -> None:
        if self.type == AsteroidType.SMALL:
            return

        match self.type:
            case AsteroidType.LARGE:
                new_type = AsteroidType.MEDIUM
            case AsteroidType.MEDIUM:
                new_type = AsteroidType.SMALL

        random_offset = random.uniform(20, 50)
        self.spawn_new_on_split(new_type, random_offset)
        self.spawn_new_on_split(new_type, -random_offset)

    def spawn_new_on_split(self, asteroid_type: AsteroidType, random_offset: float) -> None:
        new_asteroid = Asteroid(self.scene, self.position, asteroid_type)
        new_asteroid.velocity = self.velocity.rotate(random_offset)

    def _is_on_screen(self) -> bool:
        margin = 100
        screen_inflated = self.scene.screen.get_rect().inflate(margin, margin)
        return self.rect.colliderect(screen_inflated)
