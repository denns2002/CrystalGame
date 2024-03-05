import os
from random import randint
from typing import List, Tuple

import pygame
from pygame import Surface, Rect

from codes import spritesheet
from settings.settings import *


class CustomObject(pygame.sprite.Sprite):
    """
    Костомный объект, наследуемый от спрайта, объект, потому что спрайт,
    по сути, картинка, а это объект со спрайтом, коллизией, хитбоксом и т.п.

    image: Surface - картинка\n
    sprite: Surface - квадрат, в которм картинка\n
    collision: Surface - квадрат столкновения с объектами\n
    hitbox: Surface - квадрат урона\n
    object: bool - виден ли объект
    interaction: bool - можно ли взаимодействовать напрямую (не способностями)

    Позиции картинок обычно указываются по top left координатам, так удобнее.
    """

    image: Surface = None  # картинка
    sprite: Rect = None  # квадрат, в которм картинка
    collision: Rect = None  # квадрат столкновения
    hitbox: Rect = None  # квадрат урона
    visible: bool = True  # видимый объект

    def __init__(self,
                 pos,
                 z,
                 groups_dict: dict,
                 image_path=f'{SPRITES_FOLDER}notfound.png'):
        super().__init__()

        self.add(groups_dict['visible'])
        self.z = z
        self.groups = groups_dict

        """
        Если оъекта нет в словаре объектов, то будет создаваться этот
        объект без коллизии, без хитбокса и с текстурой "NotFound".
        Если у объекта много вариантов текстур и конкретный выбор не важен, то
        использовать функцию get_random_static_image.
        """
        image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image, (TILESIZE, TILESIZE))
        self.sprite = self.image.get_rect(topleft=pos)
        self.hitbox = self.sprite.inflate(0, 0)
        self.animations = {}

    def get_random_static_image(self, image_path: str) -> None:
        """
        Случайный спрайт/таблица, независимо от кол-ва спрайтов.
        Динамические вариации, например, для анимаций, вызывать не тут!

        Пример image_path:\n
        "assets/terrain/plants/trees/green_tree/green_tree"\n
        Где желит много файлов типа green_tree_8.png или 9, 22, 33 и т.п.

        Результат будет примерно таким:\n
        "assets/terrain/plants/trees/green_tree/green_tree_8.png"

        :param image_path: папка со спрайтами и файл без цифр и подчеркивания
        цифр
        :return: строка с пути картинки
        """

        count = len(os.listdir(image_path[:image_path.rfind("/")]))
        self.image = pygame.image.load(
            f'{image_path}_{randint(1, count)}.png'
        ).convert_alpha()

    def upscale_image_to_tale(self):
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))

    @staticmethod
    def set_spritesheet(self, path):
        sprite_sheet_image = pygame.image.load(path).convert_alpha()

        return spritesheet.SpriteSheet(sprite_sheet_image)

    def add_anim(self,
                 name: str,
                 frames: int,
                 spitesheet_path: str,
                 scale: int = 1,
                 flip_x: bool = False,
                 flip_y: bool = False,
                 cooldown: int = 255,
                 color: tuple | str = (155, 155, 155),
                 two_sides: bool = False):

        self.animations[name] = {}
        self.animations[name]['cooldown'] = cooldown
        self.animations[name]['sprite_sheet'] = []

        sprite_sheet_image = pygame.image.load(spitesheet_path)
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
        width, height = sprite_sheet_image.get_size()
        width = width // frames

        for i in range(flip_x, two_sides + 1):
            temp_img_list = []
            step_counter = 0
            for _ in range(frames):
                image = sprite_sheet.get_image(step_counter, width, height, scale,
                                               color, bool(i), flip_y)
                temp_img_list.append(image)
                step_counter += 1
            self.animations[name]['sprite_sheet'].append(temp_img_list)

    def run_anim(self, name: str, frame: int = 0):
        """Запускает анимацию"""

        if self.animations['now'] != name:
            self.animations['now'] = name
            self.animations['frame'] = frame
            self.animations['last_update'] = pygame.time.get_ticks()


class CollisionObject(CustomObject):

    def __init__(self, pos, z, groups_dict,
                 image_path=f'{SPRITES_FOLDER}notfound.png'):

        super().__init__(pos, z, groups_dict, image_path)
        self.add(groups_dict['collision'])
        self.collision = self.sprite.copy()
        self.has_collision = True

        self.create_debug_boxes()

    def create_debug_boxes(self):
        if self.collision:
            path = f'{SPRITES_FOLDER}collision.png'
            collision_image = pygame.image.load(path)
            self.collision_image = pygame.transform.scale(  # меняю размер дерева
                collision_image, (self.collision.height, self.collision.width)
            )


class EntityObject(CollisionObject):
    def __init__(self, pos, z, groups_dict,
                 image_path=f'{SPRITES_FOLDER}notfound.png'):

        super().__init__(pos, z, groups_dict, image_path)
        self.direction = pygame.math.Vector2()
        self.entity_collision = True

    def move(self, speed: int) -> None:
        """
        Позволяет передвигать объект
        :param speed: скорость
        """

        # Если объект двигается по диагонали, то его скорость быстрее, чем по
        # движение по осям, эти две строки фиксят этот баг
        if self.direction.magnitude():
            self.direction = self.direction.normalize()

        # перемещение, зависящие от скорости
        self.collision.x += self.direction.x * speed
        self.check_collision('x', self.groups['collision'])
        self.collision.y += self.direction.y * speed
        self.check_collision('y', self.groups['collision'])
        self.sprite.center = self.collision.center

    def check_collision(self, direction: str,
                        collision_group: pygame.sprite.Group) -> None:
        """
        Проверяет, столкнулся ли объект с другим с объектом с коллизией
        нужен direction!

        :param direction: направление
        :param collision_group: группа объектов с коллизией
        """

        def is_ghost(obj):
            ghost_bool = 'has_collision' in obj.__dict__ \
                         and (not self.has_collision or not obj.has_collision)

            entity_bool = 'entity_collision' in obj.__dict__ \
                          and (not self.entity_collision or not obj.entity_collision)
            return ghost_bool or entity_bool

        if direction == 'x':
            for obj in collision_group:

                if obj == self:
                    continue

                if obj.collision.colliderect(self.collision) and not is_ghost(obj):

                    if self.direction.x > 0:  # движение направо
                        # Чтобы спрайт игрока не входил в объектd
                        self.collision.right = obj.collision.left
                    if self.direction.x < 0:  # движение налево
                        self.collision.left = obj.collision.right

        if direction == 'y':
            for obj in collision_group:

                if obj == self:
                    continue

                if obj.collision.colliderect(self.collision) and not is_ghost(obj):
                    if self.direction.y > 0:  # движение вниз
                        self.collision.bottom = obj.collision.top
                    if self.direction.y < 0:  # движение ввех
                        self.collision.top = obj.collision.bottom
