from __future__ import annotations

from enum import IntEnum, auto
from typing import TYPE_CHECKING, override

import pygame as pg
from pygame.sprite import Group, GroupSingle

from scenes.base import BaseScene
from utils import debug_draw_rect

if TYPE_CHECKING:
    from objects import SpriteWrapper


class GameEvents(IntEnum):
    EXIT = auto()


class GameScene(BaseScene):
    @override
    def __init__(self, viewport: pg.Rect) -> None:
        super().__init__()
        self.viewport = viewport
        self._setup_groups()

    @override
    def draw(self, screen: pg.Surface) -> None:
        for obj in self.drawable:
            obj.draw(screen)

            if self._settings.debug:
                debug_draw_rect(obj, screen)

    @override
    def update(self, dt: float) -> None:
        self.updatable.update(dt)

    def get_events(self) -> set[GameEvents] | None:
        events = set()
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                events.add(GameEvents.EXIT)
        return events if events else None

    def _setup_groups(self) -> None:
        self.drawable: Group[SpriteWrapper] = Group()
        self.updatable: Group[SpriteWrapper] = Group()

        self.player: GroupSingle[SpriteWrapper] = GroupSingle()
        self.asteroids: Group[SpriteWrapper] = Group()
        self.projectiles: Group[SpriteWrapper] = Group()
