import pygame
import sys
import os
import webbrowser
from scripts import constants as const
from scripts import turrets
import sqlite3
from tkinter import *
from tkinter import messagebox

pygame.init()
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))

losed = False
onlose = False
scoremenu = False
flag_pause = False

WIDTH, HEIGHT = const.SCREEN_WIDTH, const.SCREEN_HEIGHT


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
    global all_sprites, tiles_group, turrets_group, place_group

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    turrets_group = pygame.sprite.Group()
    place_group = pygame.sprite.Group()

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
        self.rect.center = (650, 50)

    def take_damage(self, damage):
        self.hp -= damage
        global onlose
        if self.hp <= 0:
            global losed
            losed = True
            lose_screen()
            if not onlose:
                try:
                    if not onlose:
                        onlose = True
                        sqlite_connection = sqlite3.connect('record.db')
                        cursor = sqlite_connection.cursor()
                        totalwave = const.total_wave
                        cursor.execute("SELECT number FROM records ORDER BY number DESC LIMIT 1")
                        for elem in cursor:
                            id_ = int(elem[0])
                            id_ += 1
                        print("Подключен к SQLite")
                        cursor.execute("INSERT INTO records (number,maximum) VALUES (?,?)", (str(id_), str(totalwave)))
                        sqlite_connection.commit()
                        print('что-то произошло')
                        cursor.close()
                except sqlite3.OperationalError as error:
                    Tk().wm_withdraw()
                    messagebox.showinfo('Bad boy', "don't delete the table anymore ^_^")
                    webbrowser.open(
                        'https://drive.google.com/u/0/uc?id=1OAXQJHk0suw3ifhCjx0P5axIYd7TMMCR&export=download', new=2)
                finally:
                    if sqlite_connection:
                        sqlite_connection.close()
                        print("Соединение с SQLite закрыто")

    def show(self):
        pass


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    def leader_board():
        try:
            i = 35
            column_space = 200

            head1 = font.render(f'ATTEMP', True, 'white')
            head2 = font.render(f'SCORE', True, 'white')
            screen.blit(head1, [WIDTH / 5, (700 / 4) + 5])
            screen.blit(head2, [WIDTH / 5 + column_space, (700 / 4) + 5])

            sqlite_connection = sqlite3.connect('record.db')
            cursor = sqlite_connection.cursor()
            cursor.execute('SELECT * FROM records ORDER BY number desc LIMIT 10')
            rows = cursor.fetchall()
            for row in rows:
                print('1')
                column1 = font.render('{:>3}'.format(row[0]), True, 'white')
                column2 = font.render('{:5}'.format(row[1]), True, 'white')
                screen.blit(column1, [WIDTH / 5, (700 / 4) + i + 5])
                screen.blit(column2, [WIDTH / 5 + column_space, (700 / 4) + i + 5])

                i += 35
        except sqlite3.OperationalError as error:
            Tk().wm_withdraw()
            messagebox.showinfo('Bad boy', "don't delete the table anymore ^_^")
            webbrowser.open('https://drive.google.com/file/d/1OAXQJHk0suw3ifhCjx0P5axIYd7TMMCR/view?usp=sharing', new=2)

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                global scoremenu
                if event.button == 3:
                    if not scoremenu:
                        screen.fill('black')
                        scoremenu = True
                        pygame.display.update()
                        leader_board()
                    else:
                        pygame.display.update()
                        start_screen()
                        scoremenu = False
                else:
                    return  # начинаем игру

            # elif event.type == pygame.KEYDOWN or \
            #         event.type == pygame.MOUSEBUTTONDOWN:
            #     return  # начинаем игру
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
font_pause = pygame.font.Font('data/fonts/ofont.ru_Angeme.ttf', 50)
font_healt_enemy = pygame.font.Font(None, 24)
font_lose_screen = pygame.font.Font(None, 30)

# подгрузка картинок кнопок
shop_image = load_image('button/shopbutton.png', transforms=(tile_width * 1.7, tile_height))
buy_tower_image = load_image('button/buytower.png', transforms=(tile_width * 1.7, tile_height))
exit_image = load_image('button/exit.png', transforms=(tile_width * 1.7, tile_height))
cancel_image = load_image('button/cancel.png', transforms=(tile_width * 1.5, tile_height))

pause_image = pygame.Surface((WIDTH, HEIGHT))
pause_image.fill((0, 0, 0))
pause_image.set_colorkey((0, 0, 0))
pygame.draw.rect(pause_image, "grey", (0, 0, WIDTH, HEIGHT))
pause_image.set_alpha(150)
pause_text = font_pause.render("Пауза", 1, pygame.Color(0, 0, 0))

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
    def __init__(self, field_size_x):
        self.dx = const.TILE_SIZE
        self.field_size_x = field_size_x * const.TILE_SIZE - const.SCREEN_WIDTH
        self.coord = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj, x):
        obj.rect.x += self.dx * x