# Copilot Instructions

## Commands

```bash
uv run main.py              # Run the game
uv run main.py --debug      # Run with debug mode (shows hitboxes)
uv run ruff check .         # Lint
uv run ruff format .        # Format
uv run mypy .               # Type check (strict mode)
```

There is no test suite. Pre-commit hooks run ruff check and ruff format automatically on commit.

## Architecture

The game is structured into four packages:

- **`core/`** — Settings (Pydantic + `.env`), game constants, and clock
- **`objects/`** — All game entities (`Player`, `Asteroid`, `Missile`, `AsteroidField`)
- **`scenes/`** — Scene management and game event system
- **`utils/`** — Stateless handlers for input, collisions, and score persistence

**Flow:** `main.py` initializes Pygame and settings → `GameLoop` owns the main loop → `GameScene` manages sprite groups → groups are updated/drawn/collided each frame.

**Sprite hierarchy:**
```
pygame.Sprite
  └─ SpriteWrapper (ABC) — draw(screen), update(dt)
      └─ BaseObject (ABC) — adds position, rotation, radius, rect
          ├─ Player
          ├─ Asteroid
          └─ Missile
AsteroidField extends SpriteWrapper directly (no physics; just spawns asteroids)
```

**Scene owns five sprite groups:** `drawable`, `updatable`, `player` (GroupSingle), `asteroids`, `projectiles`. Objects are registered to groups by passing them as `*groups` to the constructor — e.g., `Player(*[drawable, updatable, player_group], scene=scene, ...)`.

**Collision detection** lives in `utils/collision_handler.py` and uses `pygame.sprite.groupcollide` / `spritecollide` with `collide_circle`. Results are handled back in `GameScene`.

## Conventions

- **Types:** mypy strict mode is enforced. Use `TYPE_CHECKING` guards to break circular imports. Use `@override` (from `typing`, Python 3.12+) on overriding methods.
- **Constants:** All tunable values (speeds, radii, timers, HP) live in `core/constants.py` as `UPPERCASE` module-level names. Don't inline magic numbers in game objects.
- **Settings:** Environment variables use the `AST_` prefix (e.g., `AST_SCREEN_WIDTH`). Access settings via the `get_settings()` LRU-cached function; never instantiate `Settings` directly.
- **Delta time:** All movement and timer logic is multiplied by `dt` (milliseconds). Timers count down in ms (e.g., `reload_timer -= dt`).
- **Position/rotation:** Use `pg.Vector2` for positions. Rotation is in degrees; direction vectors are computed with `.rotate(angle)`.
- **Bounds:** Asteroids and missiles call `self.kill()` when outside the viewport + 100px margin. The player wraps to the opposite edge.
- **Score:** Score points come from `AsteroidType.score` — LARGE=20, MEDIUM=50, SMALL=100. Score is tracked in `GameScene` and persisted to `highscore.json` on exit.
- **Style:** Single quotes, 100-character line length (ruff enforced).
