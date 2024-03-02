import sys

import pygame

from codes.levels.level import Level
from settings.settings import *


class Game:
    """
      ███████████████████████
     █             CRYSTAL            █
    ███████████████████████
    """

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_NAME)
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((150, 150, 150))
            self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
