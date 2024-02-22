import math

import pygame.sprite

from codes.objects.customobject import CustomObject
from project_settings import *


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

        self.collision = self.sprite.copy()
        # self.collision.x += self.collision.height
        # self.collision.height = 1
        self.hitbox = self.collision.copy()

        self.direction = pygame.math.Vector2()
        self.c_group = c_group

        # STATS
        self.speed = 3

        if DEBUG_BOXES:
            self.create_debug_boxes()

    def rotate(self, x, y):
        self.image = pygame.transform.rotate(
            self.original_image, math.degrees(
                math.atan2(x - self.sprite.x, y - self.sprite.y)
                )
            )
        self.sprite = self.image.get_rect(center=self.sprite.center)
        # new_rect = rotated_image.get_rect(center=self.sprite.center)
        # pygame.display.get_surface().blit(rotated_image, new_rect.topleft)

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
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
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
