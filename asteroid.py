from typing import override

import pygame
from pygame.math import Vector2
from pygame.surface import Surface

import constants
from circle import CircleBase


class Asteroid(CircleBase):
    def __init__(self, x: float, y: float, radius: int):
        super().__init__(x, y, radius)

        self.velocity: Vector2 = pygame.math.Vector2(0, 1)

    @override
    def draw(self, screen: Surface) -> None:
        color: str = "blue"
        center: Vector2 = self.position
        radius: int = self.radius
        width: int = 2

        self.rect = pygame.draw.circle(screen, color, center, radius, width)

    @override
    def update(self, dt: float) -> None:
        self.move(dt)

    def move(self, dt: float) -> None:
        self.position += self.velocity * constants.ASTEROID_MOVE_SPEED * dt
