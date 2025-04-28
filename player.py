import pygame
from typing import override

from circle import CircleBase
import constants


class Player(CircleBase):
    def __init__(self, x, y):
        super().__init__(x, y, constants.PLAYER_RADIUS)

        self.rotation = 0

    @override
    def draw(self, screen):
        color = "red"
        points = self.triangle()
        width = 2

        pygame.draw.polygon(screen, color, points, width)

    @override
    def update(self):
        pass

    def triangle(self):
        forward = pygame.math.Vector2(0, 1).rotate(self.rotation)
        right = pygame.math.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
