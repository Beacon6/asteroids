from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import pygame as pg
from pygame.sprite import AbstractGroup

from core import (
    OBJECT_LINE_WIDTH,
    PLAYER_HP,
    PLAYER_INVINCIBILITY_DURATION,
    PLAYER_MOVE_SPEED,
    PLAYER_RADIUS,
    PLAYER_RELOAD_SPEED,
    PLAYER_ROTATION_SPEED,
)
from objects.base import BaseObject
from objects.missile import Missile
from utils import InputHandler, entity_is_within_viewport, position_to_int_tuple

if TYPE_CHECKING:
    from scenes import GameScene

logger = logging.getLogger(__name__)


class Player(BaseObject):
    def __init__(
        self,
        *groups: AbstractGroup[Any],
        scene: GameScene,
        position: tuple[int, int],
        rotation: float = 180.0,
    ) -> None:
        super().__init__(
            *groups,
            scene=scene,
            position=pg.Vector2(position),
            rotation=rotation,
            radius=PLAYER_RADIUS,
        )
        self.hp = PLAYER_HP
        self.reload_timer = 0.0
        self.invincibility_timer = 0.0

        logger.debug('Player intialised at %s', position)

    def draw(self, screen: pg.Surface) -> None:
        color = 'red' if self.invincibility_timer <= 0 else 'yellow'
        pg.draw.polygon(screen, color, self._build_triangle(), OBJECT_LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.reload_timer -= dt
        self.invincibility_timer -= dt
        InputHandler.handle_input(self, dt)

    def move(self, dt: float, strafe: bool = False) -> None:
        rotation = self.rotation + 90.0 if strafe else self.rotation
        velocity = pg.Vector2(0, 1).rotate(rotation)
        self.position += velocity * PLAYER_MOVE_SPEED * dt
        self.rect.center = position_to_int_tuple(self.position)

        if not entity_is_within_viewport(self, self.scene.viewport):
            self.rotation += 180.0

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_ROTATION_SPEED * dt

    def shoot(self) -> None:
        missile_init_position = position_to_int_tuple(self.position)
        missile_groups = (self.scene.drawable, self.scene.updatable, self.scene.projectiles)
        Missile(
            *missile_groups,
            scene=self.scene,
            position=missile_init_position,
            rotation=self.rotation,
        )
        self.reload_timer = PLAYER_RELOAD_SPEED

    def take_damage(self) -> None:
        self.hp -= 1
        self.invincibility_timer = PLAYER_INVINCIBILITY_DURATION
        logger.debug('Player takes damage, HP is now %s', self.hp)

    def _build_triangle(self) -> tuple[pg.Vector2, pg.Vector2, pg.Vector2]:
        forward = pg.Vector2(0, 1).rotate(self.rotation)
        right = pg.Vector2(0, 1).rotate(self.rotation + 90) * PLAYER_RADIUS / 1.5
        a = self.rect.center + forward * PLAYER_RADIUS
        b = self.rect.center - forward * PLAYER_RADIUS - right
        c = self.rect.center - forward * PLAYER_RADIUS + right
        return (a, b, c)
