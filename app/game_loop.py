import logging

import pygame as pg
from pygame.sprite import groupcollide
from pygame.time import Clock

from app.objects import AsteroidField, GameScene, Player
from app.settings import get_settings

logger = logging.getLogger(__name__)


class GameLoop:
    _settings = get_settings()

    def __init__(self, debug: bool = False) -> None:
        self.game_scene = GameScene()
        logger.debug('Scene initialised')

        self.clock = Clock()
        self.dt = 0.0  # delta time

        self.running = True
        self.debug = debug

    def start(self) -> None:
        logger.debug('Starting game loop')
        # TODO: Prevent player from going out of bounds
        player = Player(self.game_scene)
        AsteroidField(self.game_scene)

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.stop()

            self.game_scene.screen.fill('black')
            self.game_scene.updatable.update(self.dt)

            player_collisions = groupcollide(
                self.game_scene.player,
                self.game_scene.asteroids,
                False,
                True,
            )
            if player_collisions:
                player.hp -= 1
                logger.info(f'Damage taken! {player.hp=}')
                if player.hp <= 0:
                    logger.info(f'{player.hp=} Game over!')
                    pg.event.post(pg.event.Event(pg.QUIT))

            missile_collisions = groupcollide(
                self.game_scene.projectiles,
                self.game_scene.asteroids,
                True,
                True,
                collided=pg.sprite.collide_circle,
            )
            if missile_collisions:
                logger.debug(missile_collisions)
                for _, val in missile_collisions.items():
                    val[0].split()

            for obj in self.game_scene.drawable:
                obj.draw()
                if self.debug:
                    pg.draw.rect(self.game_scene.screen, (255, 0, 0), obj.rect, 1)

            pg.display.flip()
            self.dt = self.clock.tick(self._settings.target_fps)  # time since last refresh (ms)

    def stop(self) -> None:
        logger.info('Stopping...')
        self.running = False
