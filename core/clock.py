import logging

import pygame as pg

from core.settings import get_settings

logger = logging.getLogger(__name__)


class GameClock:
    def __init__(self) -> None:
        logger.info('Initializing GameClock')
        self._settings = get_settings()
        self._clock = pg.time.Clock()
        self.dt = 0.0

    def tick(self) -> float:
        self.dt = self._clock.tick(self._settings.target_fps)
        return self.dt

    # TODO: Add fps display to debug
    @property
    def fps(self) -> float:
        return self._clock.get_fps()
