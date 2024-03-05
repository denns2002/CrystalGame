from codes.objects.customobject import CustomObject
from settings.settings import *


class GreenGrassWithTales(CustomObject):
    def __init__(self, pos, z, groups):
        super().__init__(pos, z, groups)
        folder = f'{SPRITES_FOLDER}terrain/ground/green_grass_with_tiles/'
        self.get_random_static_image(f'{folder}green_grass_with_tiles')
        self.upscale_image_to_tale()
        self.sprite = self.image.get_rect(center=pos)



