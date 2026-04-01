from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pygame as pg
from pygame.sprite import Group

if TYPE_CHECKING:
    from objects import Asteroid, Missile, Player

logger = logging.getLogger(__name__)


class CollisionHandler:
    @staticmethod
    def handle_missile_collisions(projectiles: Group[Missile], asteroids: Group[Asteroid]) -> int:
        hits = pg.sprite.groupcollide(
            projectiles,
            asteroids,
            True,
            True,
            collided=pg.sprite.collide_circle,
        )
        score_delta = 0
        for asteroids_hit in hits.values():
            for asteroid in asteroids_hit:
                asteroid.split()
                score_delta += asteroid.type.score
        return score_delta

    @staticmethod
    def handle_player_collisions(player: Player | None, asteroids: Group[Asteroid]) -> None:
        if not player or player.invincibility_timer > 0:
            return
        hits = pg.sprite.spritecollide(player, asteroids, True, collided=pg.sprite.collide_circle)
        for asteroid in hits:
            asteroid.split()
            player.take_damage()
