from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING

import pygame as pg

from core import BASE_DIR
from utils.input_handler import InputHandler

if TYPE_CHECKING:
    from objects import SpriteWrapper

__all__ = [
    'InputHandler',
]

HIGHSCORE_FILE = BASE_DIR / 'highscore.json'


def debug_draw_rect(entity: SpriteWrapper, screen: pg.Surface) -> None:
    color = 'red'
    line_width = 2
    pg.draw.rect(
        screen,
        color,
        entity.rect,
        line_width,
    )


def entity_is_within_viewport(entity: SpriteWrapper, viewport: pg.Rect) -> bool:
    margin = (100, 100)
    inflated_screen = viewport.inflate(*margin)
    return entity.rect.colliderect(inflated_screen)


def position_to_int_tuple(position: pg.Vector2) -> tuple[int, int]:
    return int(position.x), int(position.y)


def load_highscore() -> int:
    if not HIGHSCORE_FILE.exists():
        return 0
    with open(HIGHSCORE_FILE) as f:
        highscore: dict[str, int] = json.load(f)
        return highscore.get('highscore', 0)


def save_highscore(score: int) -> None:
    highscore_data = {'highscore': score}
    tmp_file = HIGHSCORE_FILE.with_suffix('.tmp')
    with open(tmp_file, 'w') as f:
        json.dump(highscore_data, f)
        os.replace(tmp_file, HIGHSCORE_FILE)
