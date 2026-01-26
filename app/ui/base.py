from abc import ABC, abstractmethod
from typing import Any

from pygame import freetype
from pygame.freetype import Font
from pygame.surface import Surface


class PanelBase(ABC):
    def __init__(self, render_target: Surface, font_file: str | None = None, font_size: int = 16) -> None:
        self.render_target = render_target
        self.font_file = font_file
        self.font_size = font_size
        self.font = self._setup_font()

    def _setup_font(self) -> Font:
        font = freetype.Font(self.font_file, self.font_size)
        font.antialiased = True
        return font

    @abstractmethod
    def render(self, data_source: Any | None = None) -> None:
        pass
