import pygame


class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self,
                  frame,
                  width,
                  height,
                  scale: float = 1,
                  color: tuple = (155, 155, 155),
                  flip_x: bool = False,
                  flip_y: bool = False):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        if flip_x or flip_y:
            image = pygame.transform.flip(image, flip_x, flip_y)

        image.set_colorkey(color)

        return image