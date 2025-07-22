from typing import Any, override

import pygame
from pygame.math import Vector2
from pygame.surface import Surface

from app.objects.circle import CircleBase
from app.objects.missile import Missile
from app.settings import constants


class Player(CircleBase):
    def __init__(self, x: int, y: int, collections: list[Any]) -> None:
        super().__init__(x, y, constants.PLAYER_RADIUS)

        self.rotation: float = 180
        self.collections = collections
        self.reload_timer: float = 0.0

        self.hp: int = constants.PLAYER_HP
        self.score: int = 0

    @override
    def draw(self, screen: Surface) -> None:
        color: str = 'red'
        points: list[Vector2] = self.triangle()
        width: int = 2

        self.rect = pygame.draw.polygon(screen, color, points, width)

    @override
    def update(self, dt: float) -> None:
        self.reload_timer -= dt
        key_inputs = pygame.key.get_pressed()

        if key_inputs[pygame.K_LEFT]:
            self.rotate(-dt)
        if key_inputs[pygame.K_RIGHT]:
            self.rotate(dt)

        if key_inputs[pygame.K_UP]:
            self.move(dt)
        if key_inputs[pygame.K_DOWN]:
            self.move(-dt)

        if key_inputs[pygame.K_e]:
            self.strafe(dt)
        if key_inputs[pygame.K_q]:
            self.strafe(-dt)

        if key_inputs[pygame.K_SPACE] and self.reload_timer <= 0:
            self.shoot()

    def triangle(self) -> list[Vector2]:
        forward: Vector2 = pygame.math.Vector2(0, 1).rotate(self.rotation)
        right: Vector2 = pygame.math.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a: Vector2 = self.position + forward * self.radius
        b: Vector2 = self.position - forward * self.radius - right
        c: Vector2 = self.position - forward * self.radius + right
        return [a, b, c]

    def rotate(self, dt: float) -> None:
        self.rotation += constants.PLAYER_ROTATION_SPEED * dt

    def move(self, dt: float) -> None:
        forward: Vector2 = pygame.math.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * constants.PLAYER_MOVE_SPEED * dt

    def strafe(self, dt: float) -> None:
        direction: Vector2 = pygame.math.Vector2(0, 1).rotate(self.rotation + 90)
        self.position += direction * constants.PLAYER_MOVE_SPEED * dt

    def shoot(self) -> None:
        missile = Missile(self.position.x, self.position.y, constants.MISSILE_RADIUS, self.rotation)
        missile.add(*self.collections)
        self.reload_timer = constants.PLAYER_RELOAD_SPEED
