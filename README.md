# Asteroids

A simple Asteroids-style game written in Python. Built with Pygame.

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

Display settings can be changed through an `.env` which will be loaded automatically:
```bash
SCREEN_WIDTH=1920
SCREEN_HEIGHT=1080
TARGET_FPS=60
```

## TODO

- [x] Support game settings via `.env` (e.g. screen size)
- [x] Implement asteroid splitting when hit
- [x] Add score tracking and display
- [x] Add player lives and a game over screen
- [x] Fix TODOs
- [ ] Add movement velocity
- [ ] Add weapons overheating
- [ ] Add power-ups (e.g. shield, rapid fire)
