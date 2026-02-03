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
AST_SCREEN_WIDTH=1920
AST_SCREEN_HEIGHT=1080
AST_TARGET_FPS=60
```
