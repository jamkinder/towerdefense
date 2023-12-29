import pygame
import sys
import os
from scripts import constants as const
from scripts import turrets

pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = const.FPS
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
turrets_group = pygame.sprite.Group()
place_group = pygame.sprite.Group()
button_sprites = pygame.sprite.Group()

tile_width = tile_height = const.TILE_SIZE

clicked = False
can_place_turr = None

font = pygame.font.Font('data/fonts/ofont.ru_Angeme.ttf', 35)
font_time = pygame.font.Font('data/fonts/ofont.ru_Angeme.ttf', 15)
font_wave = pygame.font.Font('data/fonts/ofont.ru_Angeme.ttf', 25)
font_lose_screen = pygame.font.Font(None, 30)

img = font.render('', True, 'BLUE')
screen.blit(img, (50, 50))
imgcastle = font.render('', True, 'RED')
wavetext = font.render('', True, 'RED')

product = None


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
    'grassfull': load_image('grassfull.png', transforms=(tile_width, tile_height))
}


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = [16 * ' ' + "Press any button to start game"]

    fon = pygame.transform.scale(load_image('logo.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 450
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def lose_screen():
    intro_text = [16 * ' ' + "You are dead"]

    screen.blit(fon_lose, (0, 0))
    text_coord = 450
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *groups):
        super().__init__(*groups)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':  # вид грязи
                Tile('empty', x, y, all_sprites)
            elif level[y][x] == 't':  # turret - башня
                Tile('gun', x, y, place_group, all_sprites)
                turret = turrets.Turret(tile_width * x, tile_height * y, 'usual')
                turrets_group.add(turret)
                all_sprites.add(turret)
            elif level[y][x] == 'p':  # place - свободное место под башню
                Tile('gun', x, y, place_group)
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
    return all_sprites, tiles_group, turrets_group, place_group


def generate_visual():
    start_screen()
    return generate_level(load_level('map.txt'))


shop_menu_image = load_image('shopram.png', transforms=(tile_width * 3.5 + 110, tile_height * 8.4))
fon_lose = pygame.transform.scale(load_image('losescreen.png'), (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))


class Button(pygame.sprite.Sprite):  # класс кнопок
    def __init__(self, x, y, image, scale, _type, products=None):
        super().__init__(button_sprites)
        self._type = _type

        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.product = products

    def update(self):  # отрисовываем кнопки и выполняем их действия
        global button_sprites, clicked, product
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self._type == 'shop':
                product = self.product
                button_sprites = pygame.sprite.Group()
                # кнопка открытия меню магазина
                Button(tile_width * 3.5 + 13, tile_height * 8.35 - 58, exit_image, 1, 'exit')
                clicked = True

            elif self._type == 'exit' or self._type == 'cancel':  # кнопка закрытия меню магазина
                button_sprites = pygame.sprite.Group()
                Button(0, 0, shop_image, 1, 'shop')
                clicked = False
                product = None

            elif self._type == 'buy':
                button_sprites = pygame.sprite.Group()
                Button(0, 0, cancel_image, 1, 'cancel')
                product = self.product
                clicked = False


class Castle(pygame.sprite.Sprite):
    def __init__(self):
        self.hp = 10
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(color=(255, 0, 0, 0.5))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - 50, HEIGHT - 75)

        self.pos = (440, 480)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            lose_screen()

    def show(self):
        pass


# группы спрайтов
castle_group = pygame.sprite.Group()
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


Button(0, 0, shop_image, 1, 'shop')  # создаем shop кнопку
