import pygame

from codes.levels.map import *
from codes.objects.objectlists import find_object
from debug.debugbar import show_debugbar
from project_settings import *


class Level:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.v_group = SortCameraGroup()  # Видимые объекты
        self.c_group = pygame.sprite.Group()  # Объекты с коллизией
        self.create_map()

    def create_map(self):
        for floor_i in range(len(MAP)):
            for row_i, row in enumerate(MAP[floor_i]):
                for col_i, col in enumerate(row):
                    x = col_i * TILESIZE
                    y = row_i * TILESIZE

                    if col == 'player':
                        self.player = find_object(col)(
                            (x, y), floor_i, [self.v_group], self.c_group
                        )
                    elif col:
                        obj = find_object(col)
                        if obj.visual and obj.interactive:
                            obj((x, y), floor_i, [self.v_group, self.c_group])
                        elif obj.visual:
                            obj((x, y), floor_i, [self.v_group])
                        elif obj.interactive:
                            obj((x, y), floor_i, [self.c_group])

    def run(self):
        """
        Обновление кадров и отрисовка
        """
        self.v_group.custom_draw(self.player)
        self.v_group.update()

        show_debugbar(self.player.direction)
        show_debugbar(self.player.collision.topleft, 0, 1)


class SortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.half_width = self.screen.get_size()[0] // 2
        self.half_height = self.screen.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        #  камера персонажа в центре экрана
        self.offset.x = player.sprite.centerx - self.half_width
        self.offset.y = player.sprite.centery - self.half_height
        pos = pygame.mouse.get_pos() + self.offset
        player.rotate(*pos)
        pygame.draw.circle(self.screen, "Red", pygame.mouse.get_pos(), 25)

        # for sprite in self.sprites():
        for floor_i in range(len(MAP)):
            sprites = [el for el in self.sprites() if el.z == floor_i]
            for obj in sorted(sprites, key=lambda obj: obj.sprite.bottom):
                offset_pos = obj.sprite.topleft - self.offset
                self.screen.blit(obj.image, offset_pos)

                if 'collision_image' in obj.__dict__:
                    self.screen.blit(obj.collision_image, obj.collision.topleft - self.offset)
                if 'hitbox_image' in obj.__dict__:
                    self.screen.blit(obj.hitbox_image, obj.hitbox.topleft - self.offset)

                if obj.sprite.top < player.sprite.centery < obj.sprite.bottom\
                        and obj.sprite.left < player.sprite.centerx < obj.sprite.right\
                        and obj.z >= player.z:
                    obj.image.convert(24)
                    obj.image.set_alpha(50)
                else:
                    obj.image.set_alpha(255)

                self.screen.blit(obj.image, offset_pos)




