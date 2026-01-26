import logging

import pygame as pg
from pygame.display import set_caption

from app.game_loop import GameLoop
from app.settings import get_settings

logger = logging.getLogger(__name__)

TITLE = 'Asteroids'


class GameCore:
    _settings = get_settings()

    def __init__(self) -> None:
        pg.init()
        logger.debug('Pygame intialised')
        set_caption(TITLE)

        logger.debug('Settings loaded')
        logger.debug(self._settings.model_dump())

        GameLoop().start()
