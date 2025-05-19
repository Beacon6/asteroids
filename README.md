# Asteroids

Simple Asteroids game written in Python with Pygame.

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

## TODO

- [x] Support game settings via `.env` (e.g. screen size)
- [x] Implement asteroid splitting when hit
- [ ] Add proper graphics
- [ ] Add score tracking and display
- [ ] Add player lives and a game over screen
- [ ] Create a main menu and pause functionality
- [ ] Add power-ups (e.g. shield, rapid fire)
- [ ] Add sound effects for shooting and collisions
