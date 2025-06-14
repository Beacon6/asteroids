from typing import Any

import pygame
from pygame.sprite import Group
from pygame.surface import Surface
from pygame.time import Clock

from app.objects import AsteroidField, Player
from app.settings import constants


class GameLoop:
    def __init__(self) -> None:
        self.settings = {
            "screen_width": constants.SCREEN_WIDTH,
            "screen_height": constants.SCREEN_HEIGHT,
            "target_fps": constants.TARGET_FPS,
        }

    def start(self) -> None:
        print(f"Starting {constants.TITLE}!")
        if constants.DEBUG:
            print(self.settings)

        pygame.init()

        screen: Surface = pygame.display.set_mode(
            (self.settings["screen_width"], self.settings["screen_height"])
        )
        pygame.display.set_caption(constants.TITLE)

        clock: Clock = pygame.time.Clock()
        dt: float = 0.0

        player, group_drawable, group_updatable, group_asteroids, group_missiles = (
            self.setup_objects()
        )

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 99):
                    print(f"Quitting {constants.TITLE}. Bye!")
                    return

            screen.fill("black")

            group_updatable.update(dt)
            for obj in group_drawable:
                obj.draw(screen)

            player_collision = pygame.sprite.spritecollideany(
                player,
                group_asteroids,
                collided=pygame.sprite.collide_circle,
            )
            if player_collision:
                print("Game over!")
                return

            missile_collision = pygame.sprite.groupcollide(
                group_missiles,
                group_asteroids,
                dokilla=True,
                dokillb=True,
                collided=pygame.sprite.collide_circle,
            )
            for obj in missile_collision.values():
                obj[0].split()

            pygame.display.flip()
            dt = float(clock.tick(constants.TARGET_FPS))  # time since last refresh (ms)

    @staticmethod
    def setup_objects() -> tuple[Any, ...]:
        group_drawable: Group[Any] = pygame.sprite.Group()
        group_updatable: Group[Any] = pygame.sprite.Group()
        group_asteroids: Group[Any] = pygame.sprite.Group()
        group_missiles: Group[Any] = pygame.sprite.Group()

        player: Player = Player(
            constants.SCREEN_WIDTH // 2,
            constants.SCREEN_HEIGHT // 2,
            collections=[group_drawable, group_updatable, group_missiles],
        )
        player.add(group_drawable, group_updatable)

        asteroid_field: AsteroidField = AsteroidField(
            [group_drawable, group_updatable, group_asteroids]
        )
        asteroid_field.add(group_updatable)

        return player, group_drawable, group_updatable, group_asteroids, group_missiles
