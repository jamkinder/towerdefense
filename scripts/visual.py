import pygame
import sys
import os

pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()


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


tile_width = tile_height = 50

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
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]

        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':  # вид грязи
                Tile('empty', x, y)
            elif level[y][x] == 't':  # turret - башня
                Tile('gun', x, y)
                Tile('turret', x, y)
            elif level[y][x] == 'p':  # place - свободное место под башню
                Tile('gun', x, y)
            elif level[y][x] == '#':  # лес
                Tile('wall', x, y)
            elif level[y][x] == 'c':  # castle - замок
                Tile('castle', x, y)
            elif level[y][x] == 'l':  # lake - озеро
                Tile('lake', x, y)
            elif level[y][x] == 'h':  # вид грязи
                Tile('grasshor', x, y)
            elif level[y][x] == ',':  # вид грязи
                Tile('grassfull', x, y)
    # вернем игрока, а также размер поля в клетках
    return all_sprites, tiles_group


def generate_visual():
    return generate_level(load_level('map.txt'))
