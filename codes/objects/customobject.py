import os
from random import randint

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
    visual: bool = True  # видимый объект
    interactive: bool = False  # есть ли взаимодействие
    move = False

    def __init__(self,
                 pos,
                 z,
                 groups,
                 image_path=f'{SPRITES_FOLDER}notfound.png',
                 folder=SPRITES_FOLDER):

        super().__init__(groups)

        """
        Если оъекта нет в словаре объектов, то будет создаваться этот
        объект без коллизии, без хитбокса и с текстурой "NotFound".
        Если у объекта много вариантов текстур и конкретный выбор не важен, то
        использовать функцию random_image.
        """
        self.z = z
        
        image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image, (TILESIZE, TILESIZE))
        self.sprite = self.image.get_rect(topleft=pos)
        self.hitbox = self.sprite.inflate(0, 0)
        self.animations = {}

    def random_image(self, image_path: str) -> None:
        """
        Случайный спрайт, независимо от кол-ва спрайтов.

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

    def create_debug_boxes(self):
        if self.collision:
            path = f'{SPRITES_FOLDER}collision.png'
            collision_image = pygame.image.load(path)
            self.collision_image = pygame.transform.scale(  # меняю размер дерева
                collision_image, (self.collision.height, self.collision.width)
            )

    @staticmethod
    def set_spritesheet(self, path):
        sprite_sheet_image = pygame.image.load(path).convert_alpha()

        return spritesheet.SpriteSheet(sprite_sheet_image)

    def add_anim(self,
                 name: str,
                 frames: int,
                 spitesheet_path: str,
                 scale: int = 1,
                 cooldown: int = 255,
                 color: tuple | str = (155, 155, 155)):

        sprite_sheet_image = pygame.image.load(spitesheet_path)
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
        width, height = sprite_sheet_image.get_size()
        width = width // frames

        step_counter = 0
        temp_img_list = []
        for _ in range(frames):
            temp_img_list.append(sprite_sheet.get_image(
                step_counter, height, width, scale, color))
            step_counter += 1

        self.animations[name] = {}
        self.animations[name]['sprite_sheet'] = temp_img_list
        self.animations[name]['cooldown'] = cooldown

    def start_anim(self, name: str, frame: int = 0):
        if self.animations['now'] != name:
            self.animations['now'] = name
            self.animations['frame'] = frame
            self.animations['last_update'] = pygame.time.get_ticks()







