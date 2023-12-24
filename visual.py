import pygame
import sys
import os
import time
from pygame.locals import *
import turret_stats
clock = pygame.time.Clock()
pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
thislevel = []
FPS = 50

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
    def update(self,*args):
        pressed = pygame.key.get_pressed()
        global thislevel
        if event.type == KEYDOWN:
            if event.key == K_d and not pygame.sprite.spritecollideany(self,vertical_borders,):
                if thislevel[(self.rect.x // 50) + 1][self.rect.y // 50] == '.' or thislevel[(self.rect.x // 50) + 1][self.rect.y // 50] == '@':
                    self.rect = self.rect.move(tile_width,
                                                0)

            if event.key == K_a and not pygame.sprite.spritecollideany(self,vertical_borders):
                if thislevel[(self.rect.x // 50) - 1][self.rect.y // 50] == '.' or thislevel[(self.rect.x // 50) - 1][self.rect.y // 50] == '@':
                    self.rect = self.rect.move(-tile_width,
                                               0)
            if event.key == K_w and not pygame.sprite.spritecollideany(self,horizontal_borders):
                if thislevel[(self.rect.x // 50)][(self.rect.y // 50) - 1] == '.' or thislevel[(self.rect.x // 50)][(self.rect.y // 50) - 1] == '@':
                    self.rect = self.rect.move(0,
                                               -tile_height)
            if event.key == K_s and not pygame.sprite.spritecollideany(self,horizontal_borders):
                if thislevel[(self.rect.x // 50)][(self.rect.y // 50) + 1] == '.' or thislevel[(self.rect.x // 50)][(self.rect.y // 50) + 1] == '@':
                    self.rect = self.rect.move(0,
                                               tile_height)
            if pygame.sprite.spritecollideany(self,horizontal_borders):
                if self.rect.y > HEIGHT // 2:
                    self.rect = self.rect.move(0,
                                               -tile_height)
                else:
                    self.rect = self.rect.move(0,
                                              tile_height)
            if pygame.sprite.spritecollideany(self,vertical_borders):
                if self.rect.x > WIDTH // 2:
                    self.rect = self.rect.move(-tile_width,
                                               0)
                else:
                    self.rect = self.rect.move(tile_width,
                                              0)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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
    return image



def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    global thislevel
    thislevel = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    return thislevel

tile_images = {
    'wall': load_image('forest.png'),
    'lake': load_image("lake.png"),
    'empty': load_image('grass.png'),
    'gun': load_image('gunplace.png'),
    'castle': load_image('newcastle.png'),
    'grasshor': load_image('grasshor.png'),
    'grassfull': load_image('grassfull.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]

        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)





player = None


# группы спрайтов
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()

class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

Border(5, 5, WIDTH - 5, 5)
Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
Border(5, 5, 5, HEIGHT - 5)
Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == 'g':
                Tile('gun',x,y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == 'c':
                Tile('castle',x,y)
            elif level[y][x] == 'l':
                Tile('lake',x,y)
            elif level[y][x] == 'h':
                Tile('grasshor',x,y)
            elif level[y][x] == ',':
                Tile('grassfull',x,y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y

player, level_x, level_y = generate_level(load_level('map.txt'))


running = True
while running:
    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False

        # отрисовка и изменение свойств объектов
        # ...

        # обновление экрана
        pygame.display.flip()
        screen.fill('Black')
        #all_sprites.draw(screen)
        tiles_group.draw(screen)
        player_group.draw(screen)
        all_sprites.update(event)
        pygame.display.update()
pygame.quit()