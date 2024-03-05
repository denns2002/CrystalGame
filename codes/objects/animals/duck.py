import math
from random import randint

import pygame.sprite

from codes.objects.customobject import EntityObject
from settings.settings import *


class Duck(EntityObject):

    def __init__(self, pos, z, groups):
        super().__init__(pos, z, groups)
        self.visual = True
        self.position = pos
        self.entity_collision = False

        self.image = pygame.image.load(  # спрайт игрока
            SPRITES_FOLDER + 'arrow.png'
        ).convert_alpha()
        self.upscale_image_to_tale()
        self.sprite = self.image.get_rect(topleft=pos)
        self.original_image = self.image.copy()

        self.collision = self.sprite.copy()
        self.hitbox = self.collision.copy()

        self.direction = pygame.math.Vector2()

        # STATS
        self.speed = 10

        self.init_animations()

        if DEBUG:
            self.create_debug_boxes()

    def init_animations(self):
        self.animations: dict = {
            'now': None,
            'frame': 0,
            'last_update': pygame.time.get_ticks(),
            'side': 1
        }

        run_path = f'{SPRITES_FOLDER}objects/animals/duck/duck_run_spritesheet.png'
        self.add_anim('run', 4, run_path, 1, two_sides=True)
        self.animations['now'] = 'run'
        self.run_anim('run')

    def random_side(self):
        if randint(0, 1):
            if randint(0, 1):
                self.direction.x += 1
            else:
                self.direction.x -= 1
        else:
            if randint(0, 1):
                self.direction.y += 1
            else:
                self.direction.y -= 1

    def update(self) -> None:
        self.random_side()
        self.move(self.speed)
