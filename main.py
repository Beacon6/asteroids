import pygame
from pygame.surface import Surface
from pygame.time import Clock

import constants
from player import Player


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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(f"Quitting {constants.TITLE}. Bye!")
                return
            if event.type == pygame.WINDOWSIZECHANGED:
                new_size: tuple[int, int] = screen.get_size()
                print(f"New window width: {new_size[0]}")
                print(f"New window height: {new_size[1]}")

        screen.fill("black")

        player: Player = Player(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2)
        player.draw(screen)

        pygame.display.flip()
        clock.tick(constants.TARGET_FPS)


if __name__ == "__main__":
    main()
