import pygame
from pygame.math import Vector2
from pygame.surface import Surface
from typing import override

from circle import CircleBase
import constants


class Player(CircleBase):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, constants.PLAYER_RADIUS)

        self.rotation: float = 0

    @override
    def draw(self, screen: Surface) -> None:
        color: str = "red"
        points: list[Vector2] = self.triangle()
        width: int = 2

        pygame.draw.polygon(screen, color, points, width)

    @override
    def update(self, dt: float) -> None:
        key_inputs = pygame.key.get_pressed()

        if key_inputs[pygame.K_LEFT] or key_inputs[pygame.K_a]:
            self.rotate(-dt)
        if key_inputs[pygame.K_RIGHT] or key_inputs[pygame.K_d]:
            self.rotate(dt)

    def triangle(self) -> list[Vector2]:
        forward: Vector2 = pygame.math.Vector2(0, 1).rotate(self.rotation)
        right: Vector2 = pygame.math.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a: Vector2 = self.position + forward * self.radius
        b: Vector2 = self.position - forward * self.radius - right
        c: Vector2 = self.position - forward * self.radius + right
        return [a, b, c]

    def rotate(self, dt: float) -> None:
        self.rotation += constants.PLAYER_ROTATION_SPEED * dt
