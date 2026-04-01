import logging

import pygame as pg

from core import GameClock, get_settings
from objects import AsteroidField, Player
from scenes import GameEvents, GameScene
from utils import ScoreHandler

logger = logging.getLogger(__name__)


class GameLoop:
    _settings = get_settings()

    def __init__(self, screen: pg.Surface) -> None:
        logger.info('Initializing GameLoop')
        self.screen = screen
        self.clock = GameClock()
        self.scene = GameScene(viewport=screen.get_rect())
        self.running = True

    def start(self) -> None:
        logger.info('Starting GameLoop')
        player_init_position = (self._settings.screen_width // 2, self._settings.screen_height // 2)
        player_groups = (self.scene.drawable, self.scene.updatable, self.scene.player)
        Player(*player_groups, scene=self.scene, position=player_init_position)
        asteroid_field_groups = (self.scene.updatable,)
        AsteroidField(*asteroid_field_groups, scene=self.scene)

        while self.running:
            self.clock.tick()
            events = self.scene.get_events()
            self._handle_events(events)
            self._handle_frame()

    def stop(self) -> None:
        logger.info('Stopping GameLoop')
        ScoreHandler.handle_highscore(self.scene.score)
        self.running = False

    def _handle_events(self, events: set[GameEvents] | None) -> None:
        if not events:
            return
        events_map = {
            GameEvents.EXIT: self.stop,
            GameEvents.GAME_OVER: self.stop,
        }
        for event in events:
            events_map[event]()

    def _handle_frame(self) -> None:
        self.screen.fill('black')
        self.scene.update(self.clock.dt)
        self.scene.draw(self.screen)
        self.scene.handle_collisions()
        pg.display.flip()
