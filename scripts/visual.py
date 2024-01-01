import pygame
import sys
import os
from scripts import constants as const
from scripts import turrets

pygame.init()
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
losed = False


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


def generate_level(level):
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    turrets_group = pygame.sprite.Group()
    place_group = pygame.sprite.Group()
    button_sprites = pygame.sprite.Group()
    castle_group = pygame.sprite.Group()
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
                Tile('gun', x, y, all_sprites, place_group)
            elif level[y][x] == '#':  # лес
                Tile('wall', x, y, tiles_group, all_sprites)
            elif level[y][x] == 'c':  # castle - замок
                Tile('castle', x, y, tiles_group, all_sprites)
            elif level[y][x] == 'l':  # lake - озеро
                Tile('lake', x, y, tiles_group, all_sprites)
            elif level[y][x] == 'h':  # вид грязи
                Tile('grasshor', x, y, all_sprites, dirt_group)
            elif level[y][x] == ',':  # вид грязи
                Tile('grassfull', x, y, all_sprites, dirt_group)
    # вернем игрока, а также размер поля в клетках
    return all_sprites, tiles_group, turrets_group, place_group


def generate_visual():
    start_screen()
    castle.hp = 10
    return generate_level(load_level('map.txt'))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *groups):
        super().__init__(*groups)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Button(pygame.sprite.Sprite):  # класс кнопок
    def __init__(self, x, y, image, scale, _type, products=None):
        super().__init__(button_sprites)
        self._type = _type
        self.image = pygame.transform.scale(image,
                                            (int(image.get_width() * scale) + 5, int(image.get_height() * scale) + 5))
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
        self.rect.center = (const.SCREEN_WIDTH - 50, const.SCREEN_HEIGHT - 75)

        self.pos = (440, 480)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            global losed
            losed = True
            lose_screen()

    def show(self):
        pass


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = [" " * 6 + "Press any button to start game"]

    fon = pygame.transform.scale(load_image('fon/logo.png'), (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    screen.blit(fon, (0, 0))
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


def lose_screen():
    global losed
    intro_text = ['                     YOU LOSE',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  "Press [down arrow] to resume the game"]

    text_coord = 150
    screen.blit(pygame.transform.scale(load_image('fon/losescreen.png'), (const.SCREEN_WIDTH, const.SCREEN_HEIGHT)),
                (0, 0))
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
turrets_group = pygame.sprite.Group()
place_group = pygame.sprite.Group()
button_sprites = pygame.sprite.Group()
castle_group = pygame.sprite.Group()
dirt_group = pygame.sprite.Group()
castle = Castle()
castle.hp = 10
castle_group.add(castle)

tile_width = tile_height = const.TILE_SIZE

clicked = False
can_place_turr = None

font = pygame.font.Font('data/fonts/ofont.ru_Angeme.ttf', 30)
font_time = pygame.font.Font('data/fonts/ofont.ru_Angeme.ttf', 15)
font_wave = pygame.font.Font('data/fonts/ofont.ru_Angeme.ttf', 25)
font_healt_enemy = pygame.font.Font(None, 24)
font_lose_screen = pygame.font.Font(None, 30)

# подгрузка картинок кнопок
shop_image = load_image('button/shopbutton.png', transforms=(tile_width * 1.7, tile_height))
buy_tower_image = load_image('button/buytower.png', transforms=(tile_width * 1.7, tile_height))
exit_image = load_image('button/exit.png', transforms=(tile_width * 1.7, tile_height))
cancel_image = load_image('button/cancel.png', transforms=(tile_width * 1.5, tile_height))

tile_images = {
    'wall': load_image('block/forest.png', transforms=(tile_width, tile_height)),
    'lake': load_image("block/lake.png", transforms=(tile_width, tile_height)),
    'empty': load_image('block/grass.png', transforms=(tile_width, tile_height)),
    'gun': load_image('block/gunplace.png', transforms=(tile_width, tile_height)),
    'castle': load_image('block/newcastle.png', transforms=(tile_width, tile_height)),
    'grasshor': load_image('block/grasshor.png', transforms=(tile_width, tile_height)),
    'grassfull': load_image('block/grassfull.png', transforms=(tile_width, tile_height))
}

product = None

shop_menu_image = load_image('fon/shopram.png', transforms=(tile_width * 4 + 110, tile_height * 8.5))
Button(0, 0, shop_image, 1, 'shop')  # создаем shop кнопку


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self,  field_size):
        self.dx = const.TILE_SIZE
        self.field_size = field_size

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj, x):
        obj.rect.x += self.dx * x

