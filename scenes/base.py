from abc import ABC, abstractmethod

import pygame as pg


class BaseScene(ABC):
    @abstractmethod
    def draw(self, screen: pg.Surface) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass
