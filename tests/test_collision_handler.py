from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from core.constants import PLAYER_INVINCIBILITY_DURATION
from objects.asteroid import AsteroidType
from utils.collision_handler import CollisionHandler


@pytest.fixture
def asteroid() -> MagicMock:
    asteroid = MagicMock()
    asteroid.type = AsteroidType.LARGE
    return asteroid


@pytest.fixture
def player() -> MagicMock:
    player = MagicMock()
    player.invincibility_timer = 0.0
    return player


def test_missile_hit_returns_score(asteroid: MagicMock, mocker: MockerFixture) -> None:
    mocker.patch(
        'pygame.sprite.groupcollide',
        return_value={'missile': [asteroid]},
    )
    result = CollisionHandler.handle_missile_collisions(MagicMock(), MagicMock())
    assert result == asteroid.type.score


def test_missile_hit_calls_split_on_asteroids(asteroid: MagicMock, mocker: MockerFixture) -> None:
    mocker.patch(
        'pygame.sprite.groupcollide',
        return_value={'missile': [asteroid]},
    )
    CollisionHandler.handle_missile_collisions(MagicMock(), MagicMock())
    asteroid.split.assert_called_once()


def test_no_missile_hits_returns_zero(mocker: MockerFixture) -> None:
    mocker.patch('pygame.sprite.groupcollide', return_value={})
    result = CollisionHandler.handle_missile_collisions(MagicMock(), MagicMock())
    assert result == 0


def test_player_none_does_not_raise() -> None:
    CollisionHandler.handle_player_collisions(None, MagicMock())


def test_invincible_player_skips_collision_check(player: MagicMock, mocker: MockerFixture) -> None:
    player.invincibility_timer = PLAYER_INVINCIBILITY_DURATION
    collision_check = mocker.patch('pygame.sprite.spritecollide')
    CollisionHandler.handle_player_collisions(player, MagicMock())
    collision_check.assert_not_called()


def test_player_hit_calls_take_damage(
    player: MagicMock,
    asteroid: MagicMock,
    mocker: MockerFixture,
) -> None:
    mocker.patch('pygame.sprite.spritecollide', return_value=[asteroid])
    CollisionHandler.handle_player_collisions(player, MagicMock())
    player.take_damage.assert_called_once()


def test_player_hit_calls_split_on_asteroid(
    player: MagicMock,
    asteroid: MagicMock,
    mocker: MockerFixture,
) -> None:
    mocker.patch('pygame.sprite.spritecollide', return_value=[asteroid])
    CollisionHandler.handle_player_collisions(player, MagicMock())
    asteroid.split.assert_called_once()
