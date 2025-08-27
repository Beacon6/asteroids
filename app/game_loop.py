from typing import Any

import pygame as pg
from pygame.sprite import Group
from pygame.surface import Surface
from pygame.time import Clock

from app.objects import AsteroidField, GameOverPanel, Player, ScorePanel
from app.utils import constants, get_logger


class GameLoop:
    logger = get_logger(__name__)
    settings = {
        'screen_width': constants.SCREEN_WIDTH,
        'screen_height': constants.SCREEN_HEIGHT,
        'target_fps': constants.TARGET_FPS,
    }

    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption('Asteroids')

        self.clock: Clock = pg.time.Clock()
        self.dt: float = 0.0
        self.screen: Surface = pg.display.set_mode((self.settings['screen_width'], self.settings['screen_height']))
        self.score_panel = ScorePanel(render_target=self.screen)
        self.game_over_panel = GameOverPanel(render_target=self.screen, font_size=64)

    def start(self) -> None:
        self.logger.info(80 * '=')
        self.logger.info(f'Starting Asteroids! {self.settings}')

        # TODO: prevent player from going out of bounds
        player, group_drawable, group_updatable, group_asteroids, group_missiles = self.setup_objects()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.logger.info('Quitting Asteroids!')
                    return

            self.screen.fill('black')
            self.score_panel.render(data_source=player)

            group_updatable.update(self.dt)
            for obj in group_drawable:
                obj.draw(self.screen)

            player_collision = pg.sprite.spritecollideany(
                player,
                group_asteroids,
                collided=pg.sprite.collide_circle,
            )
            if player_collision:
                player.hp -= 1
                player_collision.kill()  # TODO: remove the colliding asteroid object; have to rename that
                self.logger.info(f'Damage taken! {player.hp=}')
                if player.hp <= 0:
                    self.logger.info(f'{player.hp=} Game over!')
                    self.game_over_panel.render()
                    pg.event.post(pg.event.Event(pg.QUIT))

            missile_collision = pg.sprite.groupcollide(
                group_missiles,
                group_asteroids,
                dokilla=True,
                dokillb=True,
                collided=pg.sprite.collide_circle,
            )
            if missile_collision:
                for obj in missile_collision.values():
                    obj[0].split()
                    player.score += obj[0].type.score

            pg.display.flip()
            self.dt = float(self.clock.tick(constants.TARGET_FPS))  # time since last refresh (ms)

    @staticmethod
    def setup_objects() -> tuple[Any, ...]:
        group_drawable: Group[Any] = pg.sprite.Group()
        group_updatable: Group[Any] = pg.sprite.Group()
        group_asteroids: Group[Any] = pg.sprite.Group()
        group_missiles: Group[Any] = pg.sprite.Group()

        player: Player = Player(
            constants.SCREEN_WIDTH // 2,
            constants.SCREEN_HEIGHT // 2,
            collections=[group_drawable, group_updatable, group_missiles],
        )
        player.add(group_drawable, group_updatable)

        # TODO: Cleanup asteroids that are out of bounds
        asteroid_field: AsteroidField = AsteroidField([group_drawable, group_updatable, group_asteroids])
        asteroid_field.add(group_updatable)

        return player, group_drawable, group_updatable, group_asteroids, group_missiles
