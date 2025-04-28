from abc import abstractmethod

import pygame


class CircleBase(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__()

        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.radius = radius

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self):
        pass
