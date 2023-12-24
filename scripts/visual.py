import pygame
import sys
import os
from scripts import constants as const
from scripts import turrets

pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
turrets_group = pygame.sprite.Group()

tile_width = tile_height = const.TILE_SIZE


def load_image(name, colorkey=None, transforms=None):
    fullname = os.path.join('data/im', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    if transforms:
        image = pygame.transform.scale(image, transforms)
    return image


def load_level(filename):
    filename = "data/maps/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    thislevel = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    return thislevel


tile_images = {
    'wall': load_image('forest.png', transforms=(tile_width, tile_height)),
    'lake': load_image("lake.png", transforms=(tile_width, tile_height)),
    'empty': load_image('grass.png', transforms=(tile_width, tile_height)),
    'gun': load_image('gunplace.png', transforms=(tile_width, tile_height)),
    'castle': load_image('newcastle.png', transforms=(tile_width, tile_height)),
    'grasshor': load_image('grasshor.png', transforms=(tile_width, tile_height)),
    'grassfull': load_image('grassfull.png', transforms=(tile_width, tile_height)),
    'turret': load_image('archer_level_1.png', transforms=(tile_width, tile_height))
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *groups):
        super().__init__(*groups)
        self.image = tile_images[tile_type]

        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':  # вид грязи
                Tile('empty', x, y, all_sprites)
            elif level[y][x] == 't':  # turret - башня
                Tile('gun', x, y, tiles_group, all_sprites)
                turret = turrets.Turret(tile_width * x, tile_height * y, tile_images['turret'])
                turrets_group.add(turret)
                all_sprites.add(turret)
            elif level[y][x] == 'p':  # place - свободное место под башню
                Tile('gun', x, y, tiles_group, all_sprites)
            elif level[y][x] == '#':  # лес
                Tile('wall', x, y, tiles_group, all_sprites)
            elif level[y][x] == 'c':  # castle - замок
                Tile('castle', x, y, tiles_group, all_sprites)
            elif level[y][x] == 'l':  # lake - озеро
                Tile('lake', x, y, tiles_group, all_sprites)
            elif level[y][x] == 'h':  # вид грязи
                Tile('grasshor', x, y, all_sprites)
            elif level[y][x] == ',':  # вид грязи
                Tile('grassfull', x, y, all_sprites)
    # вернем игрока, а также размер поля в клетках
    return all_sprites, tiles_group, turrets_group


def generate_visual():
    return generate_level(load_level('map.txt'))
