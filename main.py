import logging

import pygame as pg

from core import CAPTION, get_settings
from game_loop import GameLoop

logger = logging.getLogger(__name__)


def setup_logging(debug: bool = False) -> None:
    log_format = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=log_level, format=log_format)


def initialize_pygame() -> pg.Surface:
    logger.info('Initializing Pygame')
    pg.init()
    pg.display.set_caption(CAPTION)
    settings = get_settings()
    resolution = (settings.screen_width, settings.screen_height)
    return pg.display.set_mode(resolution)


def main() -> None:
    logger.info('Launching %s!', CAPTION)
    settings = get_settings()
    setup_logging(settings.debug)
    logger.debug('Loaded custom settings: %s', settings.model_dump(exclude_defaults=True))

    screen = initialize_pygame()
    GameLoop(screen).start()

    logger.info('Quitting %s...', CAPTION)


if __name__ == '__main__':
    main()
