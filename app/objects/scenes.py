import logging
from abc import ABC
from typing import Any, override

from pygame.display import set_mode
from pygame.sprite import Group, GroupSingle
from pygame.surface import Surface

from app.settings import get_settings

logger = logging.getLogger(__name__)


class BaseScene(ABC):
    _settings = get_settings()

    def __init__(self) -> None:
        self.drawable: Group[Any] = Group()
        self.updatable: Group[Any] = Group()

    def draw(self, screen: Surface) -> None:
        self.drawable.draw(screen)

    def update(self, dt: float) -> None:
        self.updatable.update(dt)


class GameScene(BaseScene):
    @override
    def __init__(self) -> None:
        super().__init__()

        self.screen = set_mode((self._settings.screen_width, self._settings.screen_height))
        logger.debug('Window created')

        self.player: GroupSingle[Any] = GroupSingle()
        self.projectiles: Group[Any] = Group()
        self.asteroids: Group[Any] = Group()
