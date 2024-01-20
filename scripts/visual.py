import pygame
import sys
import os
from scripts import constants as const
from scripts import turrets

pygame.init()
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))

WIDTH, HEIGHT = const.SCREEN_WIDTH, const.SCREEN_HEIGHT


def load_image(name, colorkey=None, transforms=None):
    # загружаем изображение

    fullname = os.path.join('data/im', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    # убираем фон
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    # изменяем размер
    if transforms:
        image = pygame.transform.scale(image, transforms)
    return image


def load_level(filename):
    # загружает уровень

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
    # загрузка уровня

    # очищаем группы спрайтов
    global all_sprites, tiles_group, turrets_group, place_group
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    turrets_group = pygame.sprite.Group()
    place_group = pygame.sprite.Group()

    # обрабатываем файл и создаём карту
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':  # вид грязи
                Tile('empty', x, y, all_sprites, dirt_group)
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
    castle.rect.center = (650, 100)
    return generate_level(load_level('map.txt'))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *groups):
        super().__init__(*groups)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Button(pygame.sprite.Sprite):  # класс кнопок в магазине
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

            # кнопка открытия меню магазина
            if self._type == 'shop':
                product = self.product
                button_sprites = pygame.sprite.Group()
                clicked = True
                music_click.play()

            # кнопка закрытия меню магазина
            elif self._type == 'exit' or self._type == 'cancel':
                button_sprites = pygame.sprite.Group()
                Button(0, 0, shop_image, 1, 'shop')
                clicked = False
                product = None
                music_click.play()

            # кнопка покупки
            elif self._type == 'buy':
                button_sprites = pygame.sprite.Group()
                Button(0, 0, cancel_image, 1, 'cancel')
                product = self.product
                clicked = False
                music_click.play()

def fade(width, height):
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    for alpha in range(0, 155):
        fade.set_alpha(alpha)
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(0)



# главная башня
class Castle(pygame.sprite.Sprite):
    def __init__(self):
        self.hp = 10
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(color=(255, 0, 0, 0.5))
        self.rect = self.image.get_rect()
        self.rect.center = (650, 50)

    def take_damage(self, damage):
        # отнимаем от жизней, урон врага
        self.hp -= damage
        fade(500, 500)
        music_destruction.play()
        # если жизней не осталось, показываем экран поражения
        if self.hp <= 0:
            music_fon_game.stop()

            music_lose.play(-1)

            global losed
            losed = True
            lose_screen()


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, field_size_x):
        self.dx = const.TILE_SIZE
        self.field_size_x = field_size_x * const.TILE_SIZE - const.SCREEN_WIDTH
        self.coord = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj, x):
        obj.rect.x += self.dx * x


def terminate():
    # выходим из игры
    pygame.quit()
    sys.exit()


def start_screen():
    # стартовый экран
    intro_text = [" " * 6 + "Press any button to start game"]

    fon = pygame.transform.scale(load_image('fon/logo.png'), (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    screen.blit(fon, (0, 0))
    text_coord = 450

    # показываем текст
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
                music_fon_game.play(-1)
                return  # начинаем игру
        pygame.display.flip()


def lose_screen():
    # экран поражения
    global losed
    intro_text = [" " * 22 + 'YOU LOSE',
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

    # показываем текст
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


# создание групп спрайтов
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

# записываем размеры одной клетки
tile_width = tile_height = const.TILE_SIZE

clicked = False
losed = False
onlose = False
scoremenu = False
flag_pause = False
can_place_turr = None

# загрузка картинок шрифтов
font = pygame.font.Font('data/fonts/ofont.ru_Angeme.ttf', 30)
font_time = pygame.font.Font('data/fonts/ofont.ru_Angeme.ttf', 15)
font_text = pygame.font.Font('data/fonts/ofont.ru_Angeme.ttf', 25)
font_text_min = pygame.font.Font('data/fonts/ofont.ru_Angeme.ttf', 20)
font_pause = pygame.font.Font('data/fonts/ofont.ru_Angeme.ttf', 50)
font_healt_enemy = pygame.font.Font(None, 24)
font_lose_screen = pygame.font.Font(None, 30)

# загрузка картинок кнопок
shop_image = load_image('button/shopbutton.png', transforms=(tile_width * 1.7, tile_height))
buy_tower_image = load_image('button/buytower.png', transforms=(tile_width * 1.7, tile_height))
exit_image = load_image('button/exit.png', transforms=(tile_width * 1.7, tile_height))
cancel_image = load_image('button/cancel.png', transforms=(tile_width * 1.5, tile_height))

# загрузка музыки
music_click = pygame.mixer.Sound("data/music/click_m.wav")
music_hooked = pygame.mixer.Sound("data/music/hooked_m.wav")
music_fon_menu = pygame.mixer.Sound("data/music/fon_m.wav")
music_fon_pause = pygame.mixer.Sound("data/music/fon_pause_m.wav")
music_fon_game = pygame.mixer.Sound("data/music/fon_game_m.wav")
music_up = pygame.mixer.Sound("data/music/up_m.wav")
music_destruction = pygame.mixer.Sound("data/music/destruction_m.wav")
music_lose = pygame.mixer.Sound("data/music/lose_m.wav")


# меняем громкость музыки
music_fon_menu.set_volume(0.2)
music_fon_pause.set_volume(0.2)
music_destruction.set_volume(0.5)
music_fon_game.set_volume(0.1)

# создаём элементы из которых состоит меню паузы
pause_image = pygame.Surface((WIDTH, HEIGHT))
pause_image.fill((255, 255, 255))
pause_image.set_colorkey((255, 255, 255))
pygame.draw.rect(pause_image, "black", (0, 0, WIDTH, HEIGHT))
pause_image.set_alpha(150)
pause_text = font_pause.render("Пауза", 1, pygame.Color(255, 255, 255))

# словарь с изображениями компонентов из которых состоит карта
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

shop_menu_image = load_image('fon/shopram.png', transforms=(tile_width * 4 + 110, tile_height * 8.8))
Button(0, 0, shop_image, 1, 'shop')  # создаем shop кнопку
