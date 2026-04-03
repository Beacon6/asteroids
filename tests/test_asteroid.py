from unittest.mock import MagicMock

import pytest

from core.constants import (
    ASTEROID_LARGE_RADIUS,
    ASTEROID_LARGE_SCORE,
    ASTEROID_LARGE_SPEED,
    ASTEROID_MEDIUM_RADIUS,
    ASTEROID_MEDIUM_SCORE,
    ASTEROID_MEDIUM_SPEED,
    ASTEROID_SMALL_RADIUS,
    ASTEROID_SMALL_SCORE,
    ASTEROID_SMALL_SPEED,
)
from objects.asteroid import Asteroid, AsteroidType


@pytest.fixture
def large_asteroid(mock_scene: MagicMock) -> Asteroid:
    return Asteroid(
        mock_scene.asteroids,
        scene=mock_scene,
        position=(400, 300),
        rotation=0.0,
        asteroid_type=AsteroidType.LARGE,
    )


def test_large_type_attributes() -> None:
    assert AsteroidType.LARGE.size == ASTEROID_LARGE_RADIUS
    assert AsteroidType.LARGE.speed == ASTEROID_LARGE_SPEED
    assert AsteroidType.LARGE.score == ASTEROID_LARGE_SCORE


def test_medium_type_attributes() -> None:
    assert AsteroidType.MEDIUM.size == ASTEROID_MEDIUM_RADIUS
    assert AsteroidType.MEDIUM.speed == ASTEROID_MEDIUM_SPEED
    assert AsteroidType.MEDIUM.score == ASTEROID_MEDIUM_SCORE


def test_small_type_attributes() -> None:
    assert AsteroidType.SMALL.size == ASTEROID_SMALL_RADIUS
    assert AsteroidType.SMALL.speed == ASTEROID_SMALL_SPEED
    assert AsteroidType.SMALL.score == ASTEROID_SMALL_SCORE


def test_radius_matches_type_size(large_asteroid: Asteroid) -> None:
    assert large_asteroid.radius == ASTEROID_LARGE_RADIUS


def test_velocity_direction_at_rotation_zero(large_asteroid: Asteroid) -> None:
    assert large_asteroid.velocity.x == pytest.approx(0.0)
    assert large_asteroid.velocity.y == pytest.approx(1.0)


def test_update_moves_position_along_velocity(large_asteroid: Asteroid) -> None:
    initial_y = large_asteroid.position.y
    large_asteroid.update(100.0)
    assert large_asteroid.position.y == pytest.approx(initial_y + large_asteroid.type.speed * 100.0)


def test_update_rect_follows_position(large_asteroid: Asteroid) -> None:
    large_asteroid.update(100.0)
    assert large_asteroid.rect.centerx == int(large_asteroid.position.x)
    assert large_asteroid.rect.centery == int(large_asteroid.position.y)


def test_update_kills_when_out_of_bounds(mock_scene: MagicMock) -> None:
    asteroid = Asteroid(
        mock_scene.asteroids,
        scene=mock_scene,
        position=(-1000, -1000),
        rotation=0.0,
        asteroid_type=AsteroidType.LARGE,
    )
    assert asteroid.alive()
    asteroid.update(1.0)
    assert not asteroid.alive()


def test_small_asteroid_does_not_split(mock_scene: MagicMock) -> None:
    asteroid = Asteroid(
        mock_scene.asteroids,
        scene=mock_scene,
        position=(400, 300),
        rotation=0.0,
        asteroid_type=AsteroidType.SMALL,
    )
    mock_scene.asteroids.empty()
    asteroid.split()
    assert len(mock_scene.asteroids) == 0


def test_large_asteroid_splits_into_two_medium(
    large_asteroid: Asteroid,
    mock_scene: MagicMock,
) -> None:
    mock_scene.asteroids.empty()
    large_asteroid.split()
    children = mock_scene.asteroids.sprites()
    assert len(children) == 2
    assert all(a.type == AsteroidType.MEDIUM for a in children)


def test_medium_asteroid_splits_into_two_small(mock_scene: MagicMock) -> None:
    asteroid = Asteroid(
        mock_scene.asteroids,
        scene=mock_scene,
        position=(400, 300),
        rotation=0.0,
        asteroid_type=AsteroidType.MEDIUM,
    )
    mock_scene.asteroids.empty()
    asteroid.split()
    children = mock_scene.asteroids.sprites()
    assert len(children) == 2
    assert all(a.type == AsteroidType.SMALL for a in children)


def test_split_children_spawn_at_parent_position(
    large_asteroid: Asteroid,
    mock_scene: MagicMock,
) -> None:
    mock_scene.asteroids.empty()
    large_asteroid.split()
    for child in mock_scene.asteroids.sprites():
        assert child.position.x == pytest.approx(400, abs=1)
        assert child.position.y == pytest.approx(300, abs=1)


def test_split_children_have_correct_radius(
    large_asteroid: Asteroid,
    mock_scene: MagicMock,
) -> None:
    mock_scene.asteroids.empty()
    large_asteroid.split()
    for child in mock_scene.asteroids.sprites():
        assert child.radius == ASTEROID_MEDIUM_RADIUS
