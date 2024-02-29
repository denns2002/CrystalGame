from random import uniform

import pygame

from codes.objects.customobject import CustomObject
from project_settings import *


class GreenTree(CustomObject):
    interactive = True

    def __init__(self, pos, z, groups):
        super().__init__(pos, z, groups)

        folder = f'{SPRITES_FOLDER}terrain/plants/green_tree/'
        self.random_image(f'{folder}green_tree')  # загрузка спрайта

        factor = uniform(0.7, 1.3)  # множитель размера
        sprite_size = 2 * TILESIZE * factor  # случайный размер дерева
        self.image = pygame.transform.scale(  # меняю размер дерева
            self.image, (sprite_size, sprite_size)
        )
        self.sprite = self.image.get_rect(center=pos)

        collision_size = 0.15 * sprite_size  # размер коллизии
        self.collision = self.sprite.copy()
        self.collision.width = collision_size
        self.collision.height = collision_size
        self.collision.bottom += sprite_size - collision_size
        self.collision.right += (sprite_size - collision_size) // 2

        if DEBUG:
            self.create_debug_boxes()

