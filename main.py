from typing import Any

import pygame
from pygame.sprite import Group
from pygame.surface import Surface
from pygame.time import Clock

from objects.asteroid_field import AsteroidField
from objects.player import Player
from utils import constants


def main() -> None:
    print(f"Starting {constants.TITLE}!")
    print(f"Screen width: {constants.SCREEN_WIDTH}")
    print(f"Screen height: {constants.SCREEN_HEIGHT}")

    pygame.init()

    flags: int = pygame.RESIZABLE
    screen: Surface = pygame.display.set_mode(
        (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), flags
    )
    pygame.display.set_caption(f"{constants.TITLE}")

    clock: Clock = pygame.time.Clock()
    dt: float = 0

    player, group_drawable, group_updatable, group_asteroids = setup_objects()

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
            pygame.sprite.collide_circle,  # type: ignore[unused-ignore]
        )
        if player_collision:
            print("Game over!")
            return

        pygame.display.flip()
        dt = float(clock.tick(constants.TARGET_FPS))  # time since last refresh (ms)


def setup_objects() -> tuple[Any, ...]:
    group_drawable: Group[Any] = pygame.sprite.Group()
    group_updatable: Group[Any] = pygame.sprite.Group()
    group_asteroids: Group[Any] = pygame.sprite.Group()

    player: Player = Player(
        constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2, [group_drawable, group_updatable]
    )
    player.add(group_drawable, group_updatable)

    asteroid_field: AsteroidField = AsteroidField(
        [group_drawable, group_updatable, group_asteroids]
    )
    asteroid_field.add(group_updatable)

    return player, group_drawable, group_updatable, group_asteroids


if __name__ == "__main__":
    main()
