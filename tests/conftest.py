import os
import sys
from collections.abc import Generator
from unittest.mock import MagicMock

import pygame as pg
import pytest

from core.settings import get_settings


@pytest.fixture(scope='session', autouse=True)
def pygame_init() -> Generator[None, None, None]:
    os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
    os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
    pg.init()
    yield
    pg.quit()


@pytest.fixture(autouse=True)
def settings_reset(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    monkeypatch.setattr(sys, 'argv', ['main.py'])
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def mock_scene() -> MagicMock:
    scene = MagicMock()
    scene.viewport = pg.Rect(0, 0, 800, 600)
    scene.drawable = pg.sprite.Group()
    scene.updatable = pg.sprite.Group()
    scene.asteroids = pg.sprite.Group()
    scene.projectiles = pg.sprite.Group()
    return scene
