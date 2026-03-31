from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from objects import Player

logger = logging.getLogger(__name__)


# NOTE: Tight coupling with Player, could be refactored to return actions
class InputHandler:
    @staticmethod
    def handle_input(player: Player, dt: float) -> None:
        key_inputs = pg.key.get_pressed()

        if key_inputs[pg.K_LEFT]:
            player.rotate(-dt)
        if key_inputs[pg.K_RIGHT]:
            player.rotate(dt)

        if key_inputs[pg.K_UP]:
            player.move(dt)
        if key_inputs[pg.K_DOWN]:
            player.move(-dt)

        if key_inputs[pg.K_e]:
            player.move(dt, strafe=True)
        if key_inputs[pg.K_q]:
            player.move(-dt, strafe=True)

        if (key_inputs[pg.K_SPACE] or key_inputs[pg.K_w]) and player.reload_timer <= 0:
            logger.debug('Player shoots a missile with reload timer %s', player.reload_timer)
            player.shoot()
