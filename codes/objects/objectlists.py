"""
  ███████████████████████
 █          OBJECTS LIST          █
███████████████████████
"""
from codes.objects.animals.duck import Duck
from codes.objects.customobject import CustomObject
from codes.objects.players.player import Player
from codes.objects.terrain.ground.greengrasswithtales import GreenGrassWithTales
from codes.objects.terrain.plants.trees.green_tree import GreenTree

objects = {
    'not_found': CustomObject,
    'player': Player,
    'green_tree': GreenTree,
    'green_grass_with_tales': GreenGrassWithTales,
    'duck': Duck,
    '': None,
    # 'wall': Wall,
}


def find_object(name: str = 'not_found'):
    return objects[name] if name in objects else objects['not_found']
