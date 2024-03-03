import math

import pygame.sprite

from codes import spritesheet
from codes.objects.customobject import CustomObject
from debug.checksrpites import CheckSprites
from settings.settings import *


class Player(CustomObject):
    def __init__(self, pos, z, groups, c_group):
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

        self.direction = pygame.math.Vector2()
        self.c_group = c_group

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

    def move(self, speed: int) -> None:
        """
        Позволяет передвигать героя
        :param speed: скорость
        """

        # Если герой двигается по диагонали, то его скорость быстрее, чем по
        # движение по осям, эти две строки фиксят этот баг
        if self.direction.magnitude():
            self.direction = self.direction.normalize()

        # перемещение, зависящие от скорости
        self.collision.x += self.direction.x * speed
        self.check_collision('x')
        self.collision.y += self.direction.y * speed
        self.check_collision('y')
        self.sprite.center = self.collision.center

    def run_anim(self):
        keys = pygame.key.get_pressed()

        # TODO: поворот в сторону бега
        if any([keys[pygame.K_w],
                keys[pygame.K_s],
                keys[pygame.K_a],
                keys[pygame.K_d]]):
            if keys[pygame.K_a]:
                self.animations['side'] = 0
            self.start_anim('run')
        else:
            self.start_anim('idle')

        print(self.animations)

    def check_collision(self, direction) -> None:
        """
        Проверяет, столкнулся ли игрок с объектом с коллизией
        """
        if direction == 'x':
            for obj in self.c_group:
                if obj.collision.colliderect(self.collision):
                    if self.direction.x > 0:  # движение направо
                        # Чтобы спрайт игрока не входил в объектd
                        self.collision.right = obj.collision.left
                    if self.direction.x < 0:  # движение налево
                        self.collision.left = obj.collision.right

        if direction == 'y':
            for obj in self.c_group:
                if obj.collision.colliderect(self.collision):
                    if self.direction.y > 0:  # движение вниз
                        self.collision.bottom = obj.collision.top
                    if self.direction.y < 0:  # движение ввех
                        self.collision.top = obj.collision.bottom

    def update(self) -> None:
        self.input()
        self.move(self.speed)
        self.run_anim()
