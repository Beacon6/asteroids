import random
from enum import Enum
from typing import override

import pygame as pg
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface

from app.objects.base import ObjectBase, SpriteGroups


class AsteroidType(Enum):
    SMALL = (20, 0.1, 100)  # size, speed, score
    MEDIUM = (40, 0.05, 50)
    LARGE = (60, 0.02, 20)

    def __init__(self, size: int, speed: float, score: int) -> None:
        self.size: int = size
        self.speed: float = speed
        self.score: int = score


class Asteroid(ObjectBase):
    def __init__(self, spawn_position: Vector2, asteroid_type: AsteroidType, groups: SpriteGroups) -> None:
        super().__init__(spawn_position, groups)
        self.type: AsteroidType = asteroid_type
        self.radius: int = self.type.size
        self.velocity: Vector2 = Vector2(0, 1)

    @override
    def draw(self, screen: Surface) -> None:
        color: str = 'blue'
        width: int = 2
        self.rect: Rect = pg.draw.circle(screen, color, self.position, self.radius, width)

    @override
    def update(self, dt: float) -> None:
        self.position += self.velocity * self.type.speed * dt

    def split(self) -> None:
        if self.type == AsteroidType.SMALL:
            return

        match self.type:
            case AsteroidType.LARGE:
                new_type = AsteroidType.MEDIUM
            case AsteroidType.MEDIUM:
                new_type = AsteroidType.SMALL
        assert isinstance(new_type, AsteroidType)

        random_offset = random.uniform(20, 50)
        self._spawn_new_on_split(new_type, random_offset)
        self._spawn_new_on_split(new_type, -random_offset)

    def _spawn_new_on_split(self, asteroid_type: AsteroidType, random_offset: float) -> None:
        new_asteroid = Asteroid(
            self.position,
            asteroid_type,
            self._groups,
        )
        new_asteroid.velocity = self.velocity.rotate(random_offset)
