from pygame import freetype
from pygame.freetype import Font
from pygame.surface import Surface

from app.objects import Player


def _setup_font(size: int = 16) -> Font:
    font = freetype.Font(None, size)
    font.antialiased = True
    return font


def render_panel(dest: Surface, obj: Player) -> None:
    font = _setup_font()
    hp_text = f"Health: {obj.hp}"
    score_text = f"Score: {obj.score}"
    font.render_to(dest, (8, 8), hp_text, "green", "black")
    font.render_to(dest, (8, 32), score_text, "green", "black")
