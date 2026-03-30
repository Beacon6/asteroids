from __future__ import annotations

import logging
from enum import IntEnum, auto
from typing import TYPE_CHECKING, override

import pygame as pg
from pygame.sprite import Group, GroupSingle

from scenes.base import BaseScene
from utils import debug_draw_rect

if TYPE_CHECKING:
    from objects import Asteroid, Missile, Player, SpriteWrapper

logger = logging.getLogger(__name__)

type MissileHits = dict[Missile, list[Asteroid]]
type PlayerHits = list[Asteroid]


class GameEvents(IntEnum):
    EXIT = auto()
    GAME_OVER = auto()


class GameScene(BaseScene):
    @override
    def __init__(self, viewport: pg.Rect) -> None:
        super().__init__()
        self.viewport = viewport
        self._setup_groups()
        self.score = 0

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
        if self._handle_game_over():
            events.add(GameEvents.GAME_OVER)
        return events if events else None

    def _setup_groups(self) -> None:
        self.drawable: Group[SpriteWrapper] = Group()
        self.updatable: Group[SpriteWrapper] = Group()

        self.player: GroupSingle[Player] = GroupSingle()
        self.asteroids: Group[Asteroid] = Group()
        self.projectiles: Group[Missile] = Group()

    def handle_collisions(self) -> None:
        self._handle_missile_collisions()
        self._handle_player_collisions()

    def _handle_missile_collisions(self) -> None:
        hits: MissileHits = pg.sprite.groupcollide(
            self.projectiles,
            self.asteroids,
            True,
            True,
            collided=pg.sprite.collide_circle,
        )
        for asteroids_hit in hits.values():
            for asteroid in asteroids_hit:
                asteroid.split()
                self.score += asteroid.type.score

    def _handle_player_collisions(self) -> None:
        player = self.player.sprite
        if not player or player.invincibility_timer > 0:
            return
        hits: PlayerHits = pg.sprite.spritecollide(
            player, self.asteroids, True, collided=pg.sprite.collide_circle
        )
        for asteroid in hits:
            asteroid.split()
            player.take_damage()

    def _handle_game_over(self) -> bool:
        player = self.player.sprite
        is_game_over = player.hp <= 0
        if is_game_over:
            logger.info('Player has been destroyed')
            player.kill()
        return is_game_over
