from abc import ABC, abstractmethod

import pygame as pg

from core import get_settings


class BaseScene(ABC):
    def __init__(self) -> None:
        self._settings = get_settings()

    @abstractmethod
    def draw(self, screen: pg.Surface) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass
