"""
  ███████████████████████
 █        PROJECT SETTINGS        █
███████████████████████
"""
import os

GAME_NAME = 'Crystal'
DEFAULT_NICKNAME = 'Крестьянин'
FPS = 60
TILESIZE = 64  # размер одной клетки

# FOLDERS
SETTINGS_FOLDER = 'settings/'
SETTINGS_FILE = 'game_settings'

SPRITES_FOLDER = 'assets/'
DEBUG = True


class Settings:

    def __init__(self):
        # PLAYER
        self.nickname = DEFAULT_NICKNAME

        # DISPLAY
        self.screen_width = 1200
        self.screen_height = 800

        # KEYS

        # проверяет пользовательские настройки
        if SETTINGS_FILE in os.listdir(SETTINGS_FOLDER):
            self.set_settings(self.load_from_file(SETTINGS_FOLDER + SETTINGS_FILE))

    def __setattr__(self, key, value):
        self.save_to_file(SETTINGS_FILE)
        object.__setattr__(self, key, value)

    def set_settings(self, new_settings: dict) -> None:
        """
        Из словаря с настройками пихает новые настройки в аттрибуты
        экзмемпляра класса.

        :param new_settings: словарь с новыми настройками
        """

        for k, v in new_settings.items():
            if v.isdigit():
                v = float(v)
            setattr(self, k, v)

    @staticmethod
    def load_from_file(filename: str) -> dict:
        """
        Загружает из файла настройки и возвращает словарь с ними.

        :param filename: имя файла с настройками
        :return: словарь с настройками и их значениями
        """

        with open(filename, 'r', encoding='utf-8') as file:
            dct = {}
            while True:
                line = file.readline().rstrip()

                if not line:  # конец файла
                    break
                elif line[0] == '#':  # комментарий или заголовок
                    continue

                dct[line[:line.find('=')]] = line[line.find('=') + 1:].rstrip()

            return dct

    def save_to_file(self, filename: str) -> None:
        """
        Сохраняет настройки в файл

        :param filename: имя файла
        """

        with open(filename, 'w', encoding='utf-8') as file:
            for k, v in self.__dict__.items():
                file.write(f'{k}={v}\n')
