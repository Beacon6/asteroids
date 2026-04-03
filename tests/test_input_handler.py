from collections import defaultdict
from unittest.mock import MagicMock

import pygame as pg
import pytest
from pytest_mock import MockerFixture

from core.constants import PLAYER_RELOAD_SPEED
from utils.input_handler import InputHandler


def _make_key_state(pressed: set[int]) -> defaultdict[int, bool]:
    keys: defaultdict[int, bool] = defaultdict(bool)
    for key in pressed:
        keys[key] = True
    return keys


@pytest.fixture
def player() -> MagicMock:
    player = MagicMock()
    player.reload_timer = 0.0
    return player


def test_left_key_calls_rotate_negative(player: MagicMock, mocker: MockerFixture) -> None:
    mocker.patch('pygame.key.get_pressed', return_value=_make_key_state({pg.K_LEFT}))
    InputHandler.handle_input(player, 100.0)
    player.rotate.assert_called_once_with(-100.0)


def test_right_key_calls_rotate_positive(player: MagicMock, mocker: MockerFixture) -> None:
    mocker.patch('pygame.key.get_pressed', return_value=_make_key_state({pg.K_RIGHT}))
    InputHandler.handle_input(player, 100.0)
    player.rotate.assert_called_once_with(100.0)


def test_up_key_calls_move_forward(player: MagicMock, mocker: MockerFixture) -> None:
    mocker.patch('pygame.key.get_pressed', return_value=_make_key_state({pg.K_UP}))
    InputHandler.handle_input(player, 100.0)
    player.move.assert_called_once_with(100.0)


def test_down_key_calls_move_backward(player: MagicMock, mocker: MockerFixture) -> None:
    mocker.patch('pygame.key.get_pressed', return_value=_make_key_state({pg.K_DOWN}))
    InputHandler.handle_input(player, 100.0)
    player.move.assert_called_once_with(-100.0)


def test_e_key_calls_strafe_right(player: MagicMock, mocker: MockerFixture) -> None:
    mocker.patch('pygame.key.get_pressed', return_value=_make_key_state({pg.K_e}))
    InputHandler.handle_input(player, 100.0)
    player.move.assert_called_once_with(100.0, strafe=True)


def test_q_key_calls_strafe_left(player: MagicMock, mocker: MockerFixture) -> None:
    mocker.patch('pygame.key.get_pressed', return_value=_make_key_state({pg.K_q}))
    InputHandler.handle_input(player, 100.0)
    player.move.assert_called_once_with(-100.0, strafe=True)


def test_space_fires_when_reload_ready(player: MagicMock, mocker: MockerFixture) -> None:
    mocker.patch('pygame.key.get_pressed', return_value=_make_key_state({pg.K_SPACE}))
    InputHandler.handle_input(player, 100.0)
    player.shoot.assert_called_once()


def test_w_key_fires_when_reload_ready(player: MagicMock, mocker: MockerFixture) -> None:
    mocker.patch('pygame.key.get_pressed', return_value=_make_key_state({pg.K_w}))
    InputHandler.handle_input(player, 100.0)
    player.shoot.assert_called_once()


def test_space_does_not_fire_when_reloading(player: MagicMock, mocker: MockerFixture) -> None:
    player.reload_timer = PLAYER_RELOAD_SPEED
    mocker.patch('pygame.key.get_pressed', return_value=_make_key_state({pg.K_SPACE}))
    InputHandler.handle_input(player, 100.0)
    player.shoot.assert_not_called()
