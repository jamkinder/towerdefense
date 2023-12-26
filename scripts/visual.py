import pygame
import sys
import os
from scripts import constants as const
from scripts import turrets
import time

pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
turrets_group = pygame.sprite.Group()
tile_width = tile_height = const.TILE_SIZE
clicked = False
can_place_turr = False
font = pygame.font.SysFont(None, 44)
img = font.render('', True, 'BLUE')
screen.blit(img, (50, 50))
font2 = pygame.font.SysFont(None, 44)
imgcastle = font.render('', True, 'RED')
wavetext = font.render('', True, 'RED')


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


# подгрузка картинок кнопок
shop_image = load_image('shopbutton.png', transforms=(tile_width * 1.7, tile_height))
buy_tower_image = load_image('buytower.png', transforms=(tile_width * 1.7, tile_height))
exit_image = load_image('exit.png', transforms=(tile_width * 1.7, tile_height))
player_image = load_image('player.png', transforms=(tile_width, tile_height))
cancel_image = load_image('cancel.png', transforms=(tile_width * 1.5, tile_height))


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
                turret = turrets.Turret(tile_width * x, tile_height * y, 'usual')
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


class Button:  # класс кнопок
    def __init__(self, x, y, image, scale, type):
        self._type = type
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        shop_menu_image = load_image('shopram.png', transforms=(tile_width * 3.5, tile_height * 4))
        width = shop_menu_image.get_width()
        height = shop_menu_image.get_height()
        self.image2 = pygame.transform.scale(shop_menu_image, (int(width * 1), int(height * 1)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        global clicked
        self.clicked = clicked

    def draw(self):  # отрисовываем кнопки и выполняем их действия
        global clicked
        pos = pygame.mouse.get_pos()
        if self._type == 'shop':  # кнопка открытия меню магазина
            if self.rect.collidepoint(pos):
                self.clicked = clicked
                if pygame.mouse.get_pressed()[0] == 1 and not clicked:
                    clicked = True
                    self.clicked = True
                    screen.blit(self.image2, (self.rect.x, self.rect.y))
            # if pygame.mouse.get_pressed()[0] == 0:
            #     self.clicked = False
            if clicked:
                screen.blit(self.image2, (self.rect.x, self.rect.y))
        elif self._type == 'exit':  # кнопка закрытия меню магазина
            if self.rect.collidepoint(pos):
                self.clicked = clicked
                if pygame.mouse.get_pressed()[0] == 1 and clicked:
                    clicked = False
                    self.clicked = clicked
                    screen.blit(self.image2, (0, 0))
        elif self._type == 'buy':  # кнопка разрешает строительство башен и закрывает меню магазина
            if self.rect.collidepoint(pos):
                self.clicked = clicked
                if pygame.mouse.get_pressed()[0] == 1 and clicked:
                    clicked = False
                    self.clicked = clicked
                    screen.blit(self.image2, (0, 0))
                    global can_place_turr
                    can_place_turr = True
        elif self._type == 'cancel':
            if self.rect.collidepoint(pos):
                self.clicked = clicked
                if pygame.mouse.get_pressed()[0] == 1 and not clicked:
                    clicked = False
                    self.clicked = clicked
                    can_place_turr = False
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Castle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(color=(255, 0, 0, 0.5))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - 50, HEIGHT - 25)
        self.hp = 10
        self.pos = (440, 480)

    def take_damage(self, damage):
        self.hp -= damage

    def show(self):
        pass


# группы спрайтов
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
castle_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
castle = Castle()
castle_group.add(castle)

# class Camera:
#     # зададим начальный сдвиг камеры
#     def __init__(self):
#         self.dx = 0
#         self.dy = 0
#
#     # сдвинуть объект obj на смещение камеры
#     def apply(self, obj):
#         obj.rect.x += self.dx
#         obj.rect.y += self.dy
#
#     # позиционировать камеру на объекте target
#     def update(self, target):
#         self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
#         self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


shop_btn = Button(0, 0, shop_image, 1, 'shop')  # создаем shop кнопку
exit_btn = Button(83, 145, exit_image, 1, 'exit')
buytowerbutton = Button(10, 60, buy_tower_image, 1, 'buy')
cancelbutton = Button(0, HEIGHT - 50, cancel_image, 1, 'cancel')
