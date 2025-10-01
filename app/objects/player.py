from typing import Any, Self, override

import pygame as pg
from pygame.math import Vector2
from pygame.surface import Surface

from app.objects import Missile
from app.objects.base import ObjectBase, SpriteGroups
from app.utils import constants


class Player(ObjectBase):
    _instance: Self | None = None
    _initialized: bool = False

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance  # type: ignore

    def __init__(self, spawn_position: Vector2, groups: SpriteGroups) -> None:
        if not self._initialized:
            super().__init__(spawn_position, groups)
            self.radius: int = constants.PLAYER_RADIUS
            self.rotation: float = 180.0
            self.velocity: Vector2 = Vector2(0, 1)
            self.hp: int = constants.PLAYER_HP
            self.score: int = 0
            self.reload_timer: float = 0.0
            self._initialized = True

    def _build_triangle(self) -> list[Vector2]:
        forward: Vector2 = Vector2(0, 1).rotate(self.rotation)
        right: Vector2 = Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a: Vector2 = self.position + forward * self.radius
        b: Vector2 = self.position - forward * self.radius - right
        c: Vector2 = self.position - forward * self.radius + right
        return [a, b, c]

    @override
    def draw(self, screen: Surface) -> None:
        color: str = 'red'
        width: int = 2
        points: list[Vector2] = self._build_triangle()
        self.rect = pg.draw.polygon(screen, color, points, width)

    @override
    def update(self, dt: float) -> None:
        self.reload_timer -= dt
        key_inputs = pg.key.get_pressed()

        if key_inputs[pg.K_LEFT]:
            self.rotate(-dt)
        if key_inputs[pg.K_RIGHT]:
            self.rotate(dt)

        if key_inputs[pg.K_UP]:
            self.move(dt)
        if key_inputs[pg.K_DOWN]:
            self.move(-dt)

        if key_inputs[pg.K_e]:
            self.strafe(dt)
        if key_inputs[pg.K_q]:
            self.strafe(-dt)

        if key_inputs[pg.K_SPACE] and self.reload_timer <= 0:
            self.shoot()

    def rotate(self, dt: float) -> None:
        self.rotation += constants.PLAYER_ROTATION_SPEED * dt

    def move(self, dt: float) -> None:
        forward: Vector2 = pg.math.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * constants.PLAYER_MOVE_SPEED * dt

    def strafe(self, dt: float) -> None:
        direction: Vector2 = pg.math.Vector2(0, 1).rotate(self.rotation + 90)
        self.position += direction * constants.PLAYER_MOVE_SPEED * dt

    def shoot(self) -> None:
        Missile(self.position, self.rotation, self.groups())
        self.reload_timer = constants.PLAYER_RELOAD_SPEED
