from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pygame.math import Vector2


class Settings(BaseSettings):
    screen_width: int = 800
    screen_height: int = 600
    target_fps: int = 60

    player_radius: int = 20
    player_rotation_speed: float = 0.2
    player_move_speed: float = 0.2
    player_reload_speed: float = 300.0  # milliseconds
    player_hp: int = 3
    player_color: str = 'red'
    player_line_width: int = 2
    player_initial_rotation: float = 180.0

    missile_speed: float = 0.5
    missile_radius: int = 5
    missile_color: str = 'green'
    missile_line_width: int = 2

    asteroid_move_speed: float = 0.1
    asteroid_min_radius: int = 20
    asteroid_types_count: int = 3
    asteroid_spawn_rate: float = 1000.0  # milliseconds
    asteroid_color: str = 'blue'
    asteroid_line_width: int = 2

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_player_initial_position() -> Vector2:
    _settings = get_settings()
    w_offset = _settings.screen_width // 2
    h_offset = _settings.screen_height // 2
    return Vector2(w_offset, h_offset)


@lru_cache
def get_asteroid_max_radius() -> int:
    _settings = get_settings()
    return _settings.asteroid_min_radius * _settings.asteroid_types_count
