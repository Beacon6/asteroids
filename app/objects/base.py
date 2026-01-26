from abc import ABC, abstractmethod

from pygame.math import Vector2
from pygame.sprite import Sprite

from app.objects.scenes import GameScene
from app.settings import get_settings


class CircleBase(Sprite, ABC):
    _settings = get_settings()

    def __init__(self, scene: GameScene, position: Vector2) -> None:
        super().__init__()

        self.scene = scene

        self.position = Vector2(position)

        self.scene.drawable.add(self)
        self.scene.updatable.add(self)

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass
