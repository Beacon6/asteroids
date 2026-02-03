import pygame as pg

from core.settings import get_settings


class GameClock:
    def __init__(self) -> None:
        self._settings = get_settings()
        self._clock = pg.time.Clock()
        self.dt = 0.0

    def tick(self) -> float:
        self.dt = self._clock.tick(self._settings.target_fps) / 1000.0
        return self.dt

    @property
    def fps(self) -> float:
        return self._clock.get_fps()
