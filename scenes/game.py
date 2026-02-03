from enum import IntEnum, auto
from typing import Any, override

import pygame as pg

from scenes.base import BaseScene


class GameEvents(IntEnum):
    EXIT = auto()


class GameScene(BaseScene):
    def __init__(self) -> None:
        self.drawable: pg.sprite.Group[Any] = pg.sprite.Group()
        self.updatable: pg.sprite.Group[Any] = pg.sprite.Group()

        self.player: pg.sprite.GroupSingle[Any] = pg.sprite.GroupSingle()
        self.asteroids: pg.sprite.Group[Any] = pg.sprite.Group()
        self.projectiles: pg.sprite.Group[Any] = pg.sprite.Group()

    @override
    def draw(self, screen: pg.Surface) -> None:
        for obj in self.drawable:
            obj.draw(screen)

    @override
    def update(self, dt: float) -> None:
        self.updatable.update(dt)

    def get_events(self) -> list[GameEvents] | None:
        events = []
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                events.append(GameEvents.EXIT)

        return events if events else None
