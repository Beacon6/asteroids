from typing import Any, override

from app.objects import Player
from app.objects.base import ObjectBase
from app.ui.base import PanelBase


class ScorePanel(PanelBase):
    @override
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.h_offset = 16
        self.v_offset = 16
        self.fg_color = 'green'
        self.bg_color = 'black'

    @override
    def render(self, data_source: ObjectBase | None = None) -> None:
        assert data_source is not None and isinstance(data_source, Player)
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
