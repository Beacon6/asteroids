from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from utils.input_handler import InputHandler

if TYPE_CHECKING:
    from objects import SpriteWrapper

__all__ = [
    'InputHandler',
]


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
