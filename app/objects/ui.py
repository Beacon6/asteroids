import time
from abc import ABC, abstractmethod
from typing import override

import pygame as pg
from pygame import freetype
from pygame.freetype import Font
from pygame.surface import Surface

from app.objects.player import Player
from app.utils import constants


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
    def render(self) -> None:
        pass


class ScorePanel(PanelBase):
    @override
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.h_offset = 16
        self.v_offset = 16
        self.fg_color = 'green'
        self.bg_color = 'black'

    @override
    def render(self, data_source: Player) -> None:
        assert data_source.hp in range(1, 4)
        match data_source.hp:
            case 3:
                hp_color = self.fg_color
            case 2:
                hp_color = 'orange'
            case 1:
                hp_color = 'red'

        hp_text = f'Health: {data_source.hp}'
        score_text = f'Score: {data_source.score}'
        self.font.render_to(self.render_target, (self.h_offset, self.v_offset), hp_text, hp_color, self.bg_color)
        self.font.render_to(
            self.render_target,
            (self.h_offset, 8 + self.v_offset + self.font_size),
            score_text,
            self.fg_color,
            self.bg_color,
        )


class GameOverPanel(PanelBase):
    @override
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.h_offset = constants.SCREEN_WIDTH // 2
        self.v_offset = constants.SCREEN_HEIGHT // 2
        self.fg_color = 'purple'
        self.bg_color = 'black'

    @override
    def render(self) -> None:
        text = 'Game over!'
        text_size = self.font.get_rect(text).size
        self.font.render_to(
            self.render_target,
            (self.h_offset - text_size[0] // 2, self.v_offset - text_size[1] // 2),
            text,
            self.fg_color,
            self.bg_color,
        )
        pg.display.flip()
        time.sleep(1.0)
