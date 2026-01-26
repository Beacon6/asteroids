import time
from typing import Any, override

import pygame as pg

from app.ui.base import PanelBase


class GameOverPanel(PanelBase):
    @override
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.h_offset = 100
        self.v_offset = 100
        self.fg_color = 'purple'
        self.bg_color = 'black'

    @override
    def render(self, data_source: Any | None = None) -> None:
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
