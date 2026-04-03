from unittest.mock import MagicMock

import pytest

from core.constants import MISSILE_SPEED
from objects.missile import Missile


@pytest.fixture
def missile(mock_scene: MagicMock) -> Missile:
    return Missile(
        mock_scene.projectiles,
        scene=mock_scene,
        position=(400, 300),
        rotation=0.0,
    )


def test_velocity_at_rotation_zero(missile: Missile) -> None:
    assert missile.velocity.x == pytest.approx(0.0)
    assert missile.velocity.y == pytest.approx(1.0)


def test_velocity_at_rotation_90(mock_scene: MagicMock) -> None:
    missile = Missile(scene=mock_scene, position=(400, 300), rotation=90.0)
    assert missile.velocity.x == pytest.approx(-1.0)
    assert missile.velocity.y == pytest.approx(0.0)


def test_velocity_at_rotation_180(mock_scene: MagicMock) -> None:
    missile = Missile(scene=mock_scene, position=(400, 300), rotation=180.0)
    assert missile.velocity.x == pytest.approx(0.0)
    assert missile.velocity.y == pytest.approx(-1.0)


def test_update_moves_position_along_velocity(missile: Missile) -> None:
    initial_y = missile.position.y
    missile.update(100.0)
    assert missile.position.y == pytest.approx(initial_y + MISSILE_SPEED * 100.0)


def test_update_kills_when_out_of_bounds(mock_scene: MagicMock) -> None:
    missile = Missile(
        mock_scene.projectiles,
        scene=mock_scene,
        position=(-1000, -1000),
        rotation=0.0,
    )
    assert missile.alive()
    missile.update(1.0)
    assert not missile.alive()
