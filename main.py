import pygame

import constants
from player import Player


def main():
    print("Starting Asteroids!")
    print(f"Screen width: {constants.SCREEN_WIDTH}")
    print(f"Screen height: {constants.SCREEN_HEIGHT}")

    pygame.init()

    flags = pygame.RESIZABLE
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), flags)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting Asteroids. Bye!")
                return
            if event.type == pygame.WINDOWSIZECHANGED:
                new_size = screen.get_size()
                print(f"New window width: {new_size[0]}")
                print(f"New window height: {new_size[1]}")

        screen.fill("black")

        player = Player(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2)
        player.draw(screen)

        pygame.display.flip()
        clock.tick(constants.TARGET_FPS)


if __name__ == "__main__":
    main()
