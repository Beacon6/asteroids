import argparse
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    screen_width: int = 800
    screen_height: int = 600
    target_fps: int = 60
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_prefix='ast_',
        case_sensitive=False,
    )


def parse_cli() -> dict[str, bool]:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='run in debug mode',
    )
    return vars(parser.parse_args())


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    cli_args = parse_cli()
    return Settings(**cli_args)
