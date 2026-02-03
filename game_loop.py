import logging

import pygame as pg

from core import GameClock, get_settings
from scenes import GameEvents, GameScene

logger = logging.getLogger(__name__)


class GameLoop:
    def __init__(self, screen: pg.Surface) -> None:
        self._settings = get_settings()

        self.screen = screen
        self.clock = GameClock()
        self.scene = GameScene()
        self.running = True

    def start(self) -> None:
        logger.debug('Starting GameLoop')
        while self.running:
            self.clock.tick()
            events = self.scene.get_events()
            self._handle_events(events)

    def stop(self) -> None:
        logger.debug('Stopping GameLoop')
        self.running = False

    def _handle_events(self, events: list[GameEvents] | None) -> None:
        if not events:
            return

        events_map = {
            GameEvents.EXIT: self.stop,
        }

        for event in events:
            events_map[event]()
