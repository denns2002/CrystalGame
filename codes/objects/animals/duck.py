import math

import pygame.sprite

from codes import spritesheet
from codes.objects.customobject import CustomObject
from debug.checksrpites import CheckSprites
from settings.settings import *


class Duck(CustomObject):
    def __init__(self, pos, z, groups):
        super().__init__(pos, z, groups)
        self.visual = True
        self.position = pos

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
        self.speed = 5

        self.init_animations()

        if DEBUG:
            self.create_debug_boxes()

    def init_animations(self):
        self.animations: dict = {
            'now': None,
            'frame': 0,
            'last_update': pygame.time.get_ticks(),
            'side': 0
        }

        run_path = f'{SPRITES_FOLDER}objects/animals/duck/duck_run_spritesheet.png'
        self.add_anim('run', 4, run_path, 1)
        self.animations['now'] = 'run'
        self.start_anim('run')

