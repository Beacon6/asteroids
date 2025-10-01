import time
from typing import Any, override

import pygame as pg

from app.objects.base import ObjectBase
from app.ui.base import PanelBase
from app.utils import constants


class GameOverPanel(PanelBase):
    @override
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.h_offset = constants.SCREEN_WIDTH // 2
        self.v_offset = constants.SCREEN_HEIGHT // 2
        self.fg_color = 'purple'
        self.bg_color = 'black'

    @override
    def render(self, data_source: ObjectBase | None = None) -> None:
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
