import pygame

from codes.levels.map import *
from codes.objects.animals.duck import Duck
from codes.objects.customobject import CustomObject
from codes.objects.objectlists import find_object
from debug.checksrpites import CheckSprites
from debug.debugbar import show_debugbar
from settings.settings import *


class Level:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.v_group = VisibleObjectsGroup()  # Видимые объекты
        self.c_group = pygame.sprite.Group()  # Объекты с коллизией
        self.groups = {
            'visible': self.v_group,  # Видимые объекты
            'collision': self.c_group,  # Объекты с коллизией
            # 'hitbox' :
        }
        self.player = None
        self.clock = pygame.time.Clock()
        self.create_map()

    def create_map(self):
        for floor_i in range(len(MAP)):
            if floor_i not in self.v_group.obj_floors:
                self.v_group.obj_floors[floor_i] = []
                self.v_group.floors_count += 1

            for row_i, row in enumerate(MAP[floor_i]):
                for col_i, col in enumerate(row):
                    x = col_i * TILESIZE
                    y = row_i * TILESIZE

                    if col == 'player':
                        self.player = obj = find_object(col)(
                            (x, y), floor_i, self.groups
                        )
                    elif col:
                        obj = find_object(col)
                        obj = obj((x, y), floor_i, self.groups)
                        obj.image.convert(24)

                    self.v_group.obj_floors[floor_i].append(obj)

    def run(self):
        """
        Обновление кадров и отрисовка
        """

        self.v_group.custom_draw(self.player)
        self.v_group.update()

        # show_debugbar(self.player.direction)
        # show_debugbar(self.player.collision.topleft, 0, 1)
        show_debugbar(self.clock.get_fps(), 0, 2)
        self.clock.tick()


class VisibleObjectsGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.half_width = self.screen.get_size()[0] // 2
        self.half_height = self.screen.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.obj_floors = {}  # все видимые объекты разбитые по уровням (z коорд)
        self.floors_count = 0

    def custom_draw(self, player) -> None:
        #  камера персонажа в центре экрана
        self.offset.x = player.sprite.centerx - self.half_width
        self.offset.y = player.sprite.centery - self.half_height

        for i in range(self.floors_count):
            for obj in sorted(self.obj_floors[i], key=lambda obj: obj.sprite.bottom):
                offset_pos = obj.sprite.topleft - self.offset
                mouse_pos = pygame.mouse.get_pos() + self.offset

                if mouse_pos[0] > player.sprite.centerx:
                    player.animations['side'] = 0
                else:
                    player.animations['side'] = 1

                if isinstance(obj, Duck):
                    if mouse_pos[0] > player.sprite.centerx:
                        obj.animations['side'] = 0
                    else:
                        obj.animations['side'] = 1

                if self.check_obj_in_screen(obj, offset_pos):
                    self.do_tranpanent_obj(player, obj)
                    if obj.animations:
                        self.do_animation(obj)
                        self.screen.blit(
                            obj.animations[obj.animations['now']]
                            ['sprite_sheet'][obj.animations['side']]
                            [obj.animations['frame']],
                            offset_pos
                        )
                    else:
                        self.screen.blit(obj.image, offset_pos)

                    # if 'collision_image' in obj.__dict__:
                    #     self.screen.blit(obj.collision_image, obj.collision.topleft - self.offset)

    def check_obj_in_screen(self, obj, offset_pos) -> bool:
        """
        Проверяет в экране ли объект
        """
        scr_rect = self.screen.get_rect()

        return scr_rect.left <= offset_pos[0] + obj.sprite.width \
            and offset_pos[0] <= scr_rect.right \
            and offset_pos[1] + obj.sprite.height >= scr_rect.top \
            and offset_pos[1] - obj.sprite.height <= scr_rect.bottom

    @staticmethod
    def do_tranpanent_obj(player, obj: CustomObject) -> None:
        """
        Сделает объект перед и над игроком прозрачным
        """
        trans_alpha = 50
        full_alpha = 255

        if obj.sprite.top < player.sprite.centery < obj.sprite.bottom \
                and obj.sprite.left < player.sprite.centerx < obj.sprite.right \
                and obj.z >= player.z \
                and obj is not player:
            obj.image.set_alpha(trans_alpha)

        else:
            obj.image.set_alpha(full_alpha)

    @staticmethod
    def do_animation(obj: CustomObject):
        current_time = pygame.time.get_ticks()
        if current_time - obj.animations['last_update'] \
                >= obj.animations[obj.animations['now']]['cooldown']:
            obj.animations['frame'] += 1
            obj.animations['last_update'] = current_time

            if obj.animations['frame'] >= len(
                    obj.animations[obj.animations['now']]['sprite_sheet'][obj.animations['side']]
                    ):
                obj.animations['frame'] = 0
