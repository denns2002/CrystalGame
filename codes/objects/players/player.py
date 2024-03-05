import pygame.sprite

from codes.objects.customobject import EntityObject
from settings.settings import *


class Player(EntityObject):
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

        # TODO: поменять коллизию персонажа
        self.collision = self.sprite.copy()
        self.hitbox = self.collision.copy()

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
            'side': 1
        }
        idle_path = f'{SPRITES_FOLDER}objects/players/player_idle_spritesheet.png'
        run_path = f'{SPRITES_FOLDER}objects/players/player_run_spritesheet.png'
        self.add_anim('idle', 5, idle_path, 2, two_sides=True)
        self.add_anim('run', 5, run_path, 2, two_sides=True)
        self.animations['now'] = 'idle'

    def input(self) -> None:
        """
        Управление
        """
        keys = pygame.key.get_pressed()

        # TODO: связать кнопки с настройками
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1

        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1

        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.direction.y = 0
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.direction.x = 0

    def change_anim(self):
        keys = pygame.key.get_pressed()

        # TODO: поворот в сторону бега
        if any([keys[pygame.K_w],
                keys[pygame.K_s],
                keys[pygame.K_a],
                keys[pygame.K_d]]):
            if keys[pygame.K_a]:
                self.animations['side'] = 0
            self.run_anim('run')
        else:
            self.run_anim('idle')

    def update(self) -> None:
        self.input()
        self.move(self.speed)
        self.change_anim()
