import logging

import pygame as pg
from pygame.math import Vector2
from pygame.sprite import Sprite

from app.objects.missile import Missile
from app.objects.scenes import GameScene
from app.settings import get_player_initial_position, get_settings

logger = logging.getLogger(__name__)


class Player(Sprite):
    _settings = get_settings()

    def __init__(self, scene: GameScene) -> None:
        super().__init__()

        self.scene = scene

        self.position = get_player_initial_position()
        self.rotation = self._settings.player_initial_rotation
        logger.debug(f'Player spawn position: {self.position}/{self.rotation}')

        self.scene.drawable.add(self)
        self.scene.updatable.add(self)
        self.scene.player.add(self)

        self.hp = self._settings.player_hp
        self.score = 0
        self.reload_timer = 0.0
        logger.debug('Player initialised')

    def _build_triangle(self) -> tuple[Vector2, Vector2, Vector2]:
        forward: Vector2 = Vector2(0, 1).rotate(self.rotation)
        right: Vector2 = Vector2(0, 1).rotate(self.rotation + 90) * self._settings.player_radius / 1.5
        a: Vector2 = self.position + forward * self._settings.player_radius
        b: Vector2 = self.position - forward * self._settings.player_radius - right
        c: Vector2 = self.position - forward * self._settings.player_radius + right
        return (a, b, c)

    def draw(self) -> None:
        self.rect = pg.draw.polygon(
            self.scene.screen,
            self._settings.player_color,
            self._build_triangle(),
            self._settings.player_line_width,
        )

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
        self.rotation += self._settings.player_rotation_speed * dt

    def move(self, dt: float) -> None:
        forward: Vector2 = pg.math.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * self._settings.player_move_speed * dt

    def strafe(self, dt: float) -> None:
        direction: Vector2 = pg.math.Vector2(0, 1).rotate(self.rotation + 90)
        self.position += direction * self._settings.player_move_speed * dt

    def shoot(self) -> None:
        Missile(self.scene, self.position, self.rotation)
        self.reload_timer = self._settings.player_reload_speed
