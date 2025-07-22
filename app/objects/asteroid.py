import random
from typing import Any, override

import pygame
from pygame.math import Vector2
from pygame.surface import Surface

from app.objects.circle import CircleBase
from app.settings import constants


class Asteroid(CircleBase):
    def __init__(self, x: float, y: float, radius: int, collections: list[Any]):
        super().__init__(x, y, radius)

        self.velocity: Vector2 = pygame.math.Vector2(0, 1)
        self.collections = collections

    @override
    def draw(self, screen: Surface) -> None:
        color: str = 'blue'
        center: Vector2 = self.position
        radius: int = self.radius
        width: int = 2

        self.rect = pygame.draw.circle(screen, color, center, radius, width)

    @override
    def update(self, dt: float) -> None:
        self.move(dt)

    def move(self, dt: float) -> None:
        self.position += self.velocity * constants.ASTEROID_MOVE_SPEED * dt

    def split(self) -> None:
        if self.radius == constants.ASTEROID_MIN_RADIUS:
            return

        random_offset = random.uniform(20, 50)
        new_asteroid_a = Asteroid(
            self.position.x,
            self.position.y,
            self.radius - constants.ASTEROID_MIN_RADIUS,
            self.collections,
        )
        new_asteroid_a.velocity = self.velocity.rotate(random_offset) * 1.2
        new_asteroid_a.add(*self.collections)

        new_asteroid_b = Asteroid(
            self.position.x,
            self.position.y,
            self.radius - constants.ASTEROID_MIN_RADIUS,
            self.collections,
        )
        new_asteroid_b.velocity = self.velocity.rotate(-random_offset) * 1.2
        new_asteroid_b.add(*self.collections)
