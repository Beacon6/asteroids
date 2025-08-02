import logging
from logging import Logger

from app.game_loop import GameLoop


def main() -> None:
    logger = get_logger()

    game_loop = GameLoop(logger)
    game_loop.start()


def get_logger() -> Logger:
    logger = logging.getLogger(__name__)
    log_format = '%(asctime)s [%(levelname)s]: %(message)s'
    logging.basicConfig(filename='asteroids.log', level=logging.INFO, format=log_format)
    return logger


if __name__ == '__main__':
    main()
