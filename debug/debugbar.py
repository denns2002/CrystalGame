import pygame

pygame.init()
font = pygame.font.Font(None, 30)


def show_debugbar(info, pos_x: int = 0, pox_y: int = 0) -> None:
    """
    Показывает бар с какой-нибудь информацией, например: позиция игрока.
    Бывает, что нужно вывести несколько баров, поэтому pos_X умножится на 150,
    а pox_x на 40. Вызов будет:\n
    show_debugbar(player.direction, 0, 2)\n
    , т.е. первый столбец, вторая строка.

    :param info: выводимая информация
    :param pos_x: столбец позиции
    :param pox_y: строки позиции
    """
    screen = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, "White")
    debug_rect = debug_surf.get_rect(topleft=(pos_x*150, pox_y*40))
    pygame.draw.rect(screen, 'Black', debug_rect)

    screen.blit(debug_surf, debug_rect)
