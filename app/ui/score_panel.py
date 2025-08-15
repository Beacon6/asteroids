from pygame import freetype
from pygame.freetype import Font
from pygame.surface import Surface

from app.objects.player import Player


class ScorePanel:
    def __init__(self, render_target: Surface, font_file: str | None = None, font_size: int = 16) -> None:
        self.render_target = render_target
        self.font_file = font_file
        self.font_size = font_size
        self.font = self._setup_font()

    def _setup_font(self) -> Font:
        font = freetype.Font(self.font_file, self.font_size)
        font.antialiased = True
        return font

    def render(self, data_source: Player) -> None:
        hp_text = f'Health: {data_source.hp}'
        score_text = f'Score: {data_source.score}'
        self.font.render_to(self.render_target, (8, 8), hp_text, 'green', 'black')
        self.font.render_to(self.render_target, (8, 32), score_text, 'green', 'black')
