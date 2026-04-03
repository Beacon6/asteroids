from unittest.mock import MagicMock

import pytest

from core.constants import (
    PLAYER_HP,
    PLAYER_INVINCIBILITY_DURATION,
    PLAYER_MOVE_SPEED,
    PLAYER_RELOAD_SPEED,
    PLAYER_ROTATION_SPEED,
)
from objects.player import Player


@pytest.fixture
def player(mock_scene: MagicMock) -> Player:
    return Player(
        mock_scene.drawable,
        mock_scene.updatable,
        scene=mock_scene,
        position=(400, 300),
        rotation=180.0,
    )


def test_initial_hp(player: Player) -> None:
    assert player.hp == PLAYER_HP


def test_initial_timers_zero(player: Player) -> None:
    assert player.reload_timer == 0.0
    assert player.invincibility_timer == 0.0


def test_rotate_increases_rotation(player: Player) -> None:
    player.rotate(100.0)
    assert player.rotation == pytest.approx(180.0 + PLAYER_ROTATION_SPEED * 100.0)


def test_rotate_negative_decreases_rotation(player: Player) -> None:
    player.rotate(-100.0)
    assert player.rotation == pytest.approx(180.0 - PLAYER_ROTATION_SPEED * 100.0)


# NOTE: Y axis is inverted in Pygame
def test_move_forward_changes_position(player: Player) -> None:
    initial_y = player.position.y
    player.move(100.0)
    assert player.position.y == pytest.approx(initial_y - PLAYER_MOVE_SPEED * 100.0)


def test_move_backward_changes_position(player: Player) -> None:
    initial_y = player.position.y
    player.move(-100.0)
    assert player.position.y == pytest.approx(initial_y + PLAYER_MOVE_SPEED * 100.0)


def test_move_strafe_right_changes_position(player: Player) -> None:
    initial_x = player.position.x
    player.move(100.0, strafe=True)
    assert player.position.x == pytest.approx(initial_x + PLAYER_MOVE_SPEED * 100.0)


def test_move_strafe_left_changes_position(player: Player) -> None:
    initial_x = player.position.x
    player.move(-100.0, strafe=True)
    assert player.position.x == pytest.approx(initial_x - PLAYER_MOVE_SPEED * 100.0)


def test_move_flips_rotation_when_out_of_bounds(mock_scene: MagicMock) -> None:
    player = Player(scene=mock_scene, position=(-1000, -1000), rotation=90.0)
    player.move(1.0)
    assert player.rotation == pytest.approx(270.0)


def test_take_damage_decrements_hp(player: Player) -> None:
    initial_hp = player.hp
    player.take_damage()
    assert player.hp == initial_hp - 1


def test_take_damage_sets_invincibility_timer(player: Player) -> None:
    player.take_damage()
    assert player.invincibility_timer == pytest.approx(PLAYER_INVINCIBILITY_DURATION)


def test_shoot_sets_reload_timer(player: Player) -> None:
    player.shoot()
    assert player.reload_timer == pytest.approx(PLAYER_RELOAD_SPEED)


def test_shoot_creates_missile_in_projectiles_group(player: Player, mock_scene: MagicMock) -> None:
    player.shoot()
    assert len(mock_scene.projectiles) == 1


def test_update_decrements_reload_timer(player: Player) -> None:
    player.reload_timer = PLAYER_RELOAD_SPEED
    player.update(100.0)
    assert player.reload_timer == pytest.approx(PLAYER_RELOAD_SPEED - 100.0)


def test_update_decrements_invincibility_timer(player: Player) -> None:
    player.invincibility_timer = PLAYER_INVINCIBILITY_DURATION
    player.update(100.0)
    assert player.invincibility_timer == pytest.approx(PLAYER_INVINCIBILITY_DURATION - 100.0)
