# Asteroids

Asteroids game written with Pygame.

## Running the game

### Using [`uv`](https://github.com/astral-sh/uv):

```shell
uv run main.py
```

### Or with `pip`:

```shell
pip install -r requirements.txt
python main.py
```

## Controls

```text
↑ / ↓       Move forward / backward
← / →       Turn left / right
Q / E       Strafe left / right
Space       Shoot
Ctrl + C    Exit
```

## Settings

It is possible to change some rendering options via an `.env` file in the root directory.\
Available options are:

```
SCREEN_WIDTH     Default: 1280
SCREEN_HEIGHT    Default: 720
TARGET_FPS       Default: 60
```

## TODO

- [x] Support game settings via `.env` (e.g. screen size)
- [x] Implement asteroid splitting when hit
- [x] Add score tracking and display
- [x] Add player lives and a game over screen
- [ ] Add movement velocity
- [ ] Add weapons overheating
- [ ] Add power-ups (e.g. shield, rapid fire)
