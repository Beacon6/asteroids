import random
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, override

import pygame as pg
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface


class AsteroidType(Enum):
    SMALL = (20, 0.1, 100)  # size, speed, score
    MEDIUM = (40, 0.05, 50)
    LARGE = (60, 0.02, 20)

    def __init__(self, size: int, speed: float, score: int) -> None:
        self.size: int = size
        self.speed: float = speed
        self.score: int = score


class AsteroidBase(ABC, Sprite):
    def __init__(self, spawn_position: Vector2, asteroid_type: AsteroidType) -> None:
        super().__init__()
        self.type: AsteroidType = asteroid_type
        self.radius: int = asteroid_type.size  # radius atribute is required by Pygame for collision detection
        self.position: Vector2 = Vector2(spawn_position)
        self.velocity: Vector2 = Vector2(0, 1)

    @abstractmethod
    def draw(self, screen: Surface) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass


class Asteroid(AsteroidBase):
    def __init__(self, spawn_position: Vector2, asteroid_type: AsteroidType, collections: list[Any]) -> None:
        super().__init__(spawn_position, asteroid_type)
        self.collections = collections

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
            self.collections,
        )
        new_asteroid.velocity = self.velocity.rotate(random_offset)
        new_asteroid.add(*self.collections)
