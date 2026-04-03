from unittest.mock import MagicMock

import pygame as pg
import pytest
from pytest_mock import MockerFixture

from core.constants import ASTEROID_LARGE_RADIUS, ASTEROID_SPAWN_RATE
from objects.asteroid import AsteroidType
from objects.asteroid_field import AsteroidField


@pytest.fixture
def field(mock_scene: MagicMock) -> AsteroidField:
    return AsteroidField(mock_scene.updatable, scene=mock_scene)


def test_initial_spawn_timer(field: AsteroidField) -> None:
    assert field.spawn_timer == ASTEROID_SPAWN_RATE


def test_spawn_points_count(field: AsteroidField) -> None:
    assert len(field.spawn_points) == 4


def test_update_decrements_spawn_timer(field: AsteroidField) -> None:
    field.spawn_timer = 500.0
    field.update(100.0)
    assert field.spawn_timer == pytest.approx(400.0)


def test_update_does_not_spawn_when_timer_positive(
    field: AsteroidField,
    mocker: MockerFixture,
) -> None:
    field.spawn_timer = 500.0
    spawn_mock = mocker.patch.object(field, '_spawn')
    field.update(100.0)
    spawn_mock.assert_not_called()


def test_update_spawns_when_timer_expires(field: AsteroidField, mocker: MockerFixture) -> None:
    field.spawn_timer = 50.0
    spawn_mock = mocker.patch.object(field, '_spawn')
    field.update(100.0)
    spawn_mock.assert_called_once()


def test_left_spawn_point_position(field: AsteroidField) -> None:
    _, position_fn = field.spawn_points[0]
    pos = position_fn(0.5)
    assert pos.x == pytest.approx(-ASTEROID_LARGE_RADIUS)
    assert pos.y == pytest.approx(0.5 * 600)


def test_right_spawn_point_position(field: AsteroidField) -> None:
    _, position_fn = field.spawn_points[1]
    pos = position_fn(0.5)
    assert pos.x == pytest.approx(800 + ASTEROID_LARGE_RADIUS)
    assert pos.y == pytest.approx(0.5 * 600)


def test_bottom_spawn_point_position(field: AsteroidField) -> None:
    _, position_fn = field.spawn_points[2]
    pos = position_fn(0.5)
    assert pos.x == pytest.approx(0.5 * 800)
    assert pos.y == pytest.approx(600 + ASTEROID_LARGE_RADIUS)


def test_top_spawn_point_position(field: AsteroidField) -> None:
    _, position_fn = field.spawn_points[3]
    pos = position_fn(0.5)
    assert pos.x == pytest.approx(0.5 * 800)
    assert pos.y == pytest.approx(-ASTEROID_LARGE_RADIUS)


def test_spawn_method_resets_timer(field: AsteroidField) -> None:
    field.spawn_timer = 0.0
    field._spawn(AsteroidType.LARGE, (400, 300), pg.Vector2(1, 0))
    assert field.spawn_timer == pytest.approx(ASTEROID_SPAWN_RATE)
