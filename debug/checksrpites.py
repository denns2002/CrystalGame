import sys

import pygame

from codes.objects.customobject import CustomObject
from settings.settings import *


class CheckSprites:
    def __init__(self, obj: CustomObject, name: str = 'idle', side: int = 0):
        pygame.init()
        pygame.display.set_caption('check')
        self.screen = pygame.display.set_mode(
            (700, 300)
        )
        self.clock = pygame.time.Clock()

        self.name = name
        self.side = side
        self.obj = obj

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((150, 150, 150))

            x = 0
            y = 0

            for frame in self.obj.animations[self.name]['sprite_sheet'][self.side]:
                self.screen.blit(frame, (x, y))
                x += 100


            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = CheckSprites()
    game.run()
