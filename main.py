import logging

import pygame as pg

from core import get_settings
from game_loop import GameLoop

CAPTION = 'Asteroids'

logger = logging.getLogger(__name__)
settings = get_settings()


def main() -> None:
    logger.info('Launching %s!', CAPTION)
    logger.debug('Loaded settings: %s', settings.model_dump(exclude_defaults=True))

    pg.init()
    pg.display.set_caption(CAPTION)
    resolution = (settings.screen_width, settings.screen_height)
    screen = pg.display.set_mode(resolution)
    GameLoop(screen).start()

    logger.info('Quitting %s...', CAPTION)


if __name__ == '__main__':
    log_format = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    log_level = logging.DEBUG if settings.debug else logging.INFO
    logging.basicConfig(level=log_level, format=log_format)

    main()
