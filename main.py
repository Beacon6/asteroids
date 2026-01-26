import argparse
import logging

from app.core import GameCore

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help='Run in debug mode')
args = parser.parse_args()


def main() -> None:
    logger.info('Launching...')
    GameCore(args.debug)


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    log_format = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, format=log_format)

    main()
