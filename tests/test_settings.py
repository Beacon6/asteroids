import sys

import pytest

from core.settings import Settings, get_settings, parse_cli


def test_default_screen_width() -> None:
    assert Settings(_env_file=None).screen_width == 800  # type: ignore[call-arg]


def test_default_screen_height() -> None:
    assert Settings(_env_file=None).screen_height == 600  # type: ignore[call-arg]


def test_default_target_fps() -> None:
    assert Settings(_env_file=None).target_fps == 60  # type: ignore[call-arg]


def test_default_debug_false() -> None:
    assert Settings(_env_file=None).debug is False  # type: ignore[call-arg]


def test_env_var_overrides_screen_width(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('AST_SCREEN_WIDTH', '1920')
    assert Settings(_env_file=None).screen_width == 1920  # type: ignore[call-arg]


def test_env_var_overrides_screen_height(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('AST_SCREEN_HEIGHT', '1080')
    assert Settings(_env_file=None).screen_height == 1080  # type: ignore[call-arg]


def test_env_var_overrides_target_fps(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('AST_TARGET_FPS', '120')
    assert Settings(_env_file=None).target_fps == 120  # type: ignore[call-arg]


def test_env_var_overrides_debug(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('AST_DEBUG', 'True')
    assert Settings(_env_file=None).debug is True  # type: ignore[call-arg]


def test_parse_cli_no_debug() -> None:
    assert parse_cli() == {'debug': False}


def test_parse_cli_long_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, 'argv', ['main.py', '--debug'])
    assert parse_cli() == {'debug': True}


def test_parse_cli_short_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, 'argv', ['main.py', '-d'])
    assert parse_cli() == {'debug': True}


def test_get_settings_returns_cached_instance() -> None:
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2


def test_get_settings_debug_from_cli(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, 'argv', ['main.py', '--debug'])
    assert get_settings().debug is True
