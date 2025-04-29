from abc import abstractmethod
import pygame
from pygame.math import Vector2
from pygame.surface import Surface


class CircleBase(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, radius: int) -> None:
        super().__init__()

        self.position: Vector2 = pygame.math.Vector2(x, y)
        self.velocity: Vector2 = pygame.math.Vector2(0, 0)
        self.radius: int = radius

    @abstractmethod
    def draw(self, screen: Surface) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass
