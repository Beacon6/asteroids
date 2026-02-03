from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Core
    screen_width: int = 800
    screen_height: int = 600
    target_fps: int = 60
    debug: bool = False

    # Player
    player_radius: int = 20
    player_move_speed: float = 0.2
    player_rotation_speed: float = 0.2
    player_reload_speed: float = 300.0  # milliseconds

    # Missile
    missile_radius: int = 5
    missile_speed: float = 0.5

    # Asteroid
    asteroid_min_radius: int = 20
    asteroid_max_radius: int = 60
    asteroid_move_speed: float = 0.1
    asteroid_spawn_rate: float = 1000.0  # milliseconds

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_prefix='ast_',
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
